import re


class ContextBuilder:
    def __init__(self, all_functions, all_classes):
       
        self.all_functions = all_functions
        self.all_classes = all_classes
        self._func_by_name = {}

        for f in all_functions:
            self._func_by_name.setdefault(f["name"], []).append(f)

        self._class_by_name = {c["name"]: c for c in all_classes}
        self._all_func_names = set(self._func_by_name.keys())
        self._all_class_names = set(self._class_by_name.keys())

    def build_context(self, query, semantic_top_results=None):
        intent, target_name = self._detect_intent(query)
        
        if intent == "class" and target_name:
            primary = self._lookup_class(target_name)
            all_methods = primary.get("methods", []) if primary else []
            deps = self._expand_dependencies(all_methods)
            callers = self._find_callers([m["name"] for m in all_methods])
            return self._pack(intent, [primary] if primary else [], deps, callers)

        elif intent == "function" and target_name:
            primary = self._lookup_function(target_name)
            deps = self._expand_dependencies(primary)
            callers = self._find_callers([f["name"] for f in primary])
            return self._pack(intent, primary, deps, callers)

        else:
            if not semantic_top_results:
                return self._pack("vague", [], [], [])
            primary = [item for _, item in semantic_top_results]
            deps = self._expand_dependencies(primary)
            callers = self._find_callers([f["name"] for f in primary])
            return self._pack("vague", primary, deps, callers)


    def _detect_intent(self, query):
        tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", query))

        for token in tokens:
            if token in self._all_class_names:
                return "class", token

        for token in tokens:
            if token in self._all_func_names:
                return "function", token

        return "vague", None

    def _lookup_function(self, name):
        """Returns list of all function dicts matching the name (may span multiple files)."""
        return self._func_by_name.get(name, [])

    def _lookup_class(self, name):
        """Returns the class dict (with embedded methods) or None."""
        return self._class_by_name.get(name)

    def _expand_dependencies(self, func_list):
        """
        Given a list of function dicts, look up every function name
        that appears in their calls lists and return those dicts.

        Avoids returning functions that are already in func_list.
        """
        already_included = {f["name"] for f in func_list}
        deps = []
        seen = set()

        for func in func_list:
            for called_name in func.get("calls", []):
                if called_name in already_included or called_name in seen:
                    continue
                matches = self._func_by_name.get(called_name, [])
                deps.extend(matches)
                seen.add(called_name)

        return deps

    def _find_callers(self, target_names):
        """
        Returns all functions in the repo that call any of the target_names.
        Useful for showing "who uses this function".
        """
        target_set = set(target_names)
        callers = []
        for func in self.all_functions:
            if set(func.get("calls", [])) & target_set:
                callers.append(func)
        return callers

    def _pack(self, intent, primary, dependencies, callers):
        """Assembles the final context dict including the formatted prompt string."""
        prompt_context = self._format_prompt_context(intent, primary, dependencies, callers)
        return {
            "intent": intent,
            "primary": primary,
            "dependencies": dependencies,
            "callers": callers,
            "prompt_context": prompt_context,
        }

    def _format_prompt_context(self, intent, primary, dependencies, callers):
        """
        Builds the string you inject directly into your Gemini prompt.
        Sections are clearly labelled so Gemini understands the relationships.
        """
        parts = []

        if intent == "class" and primary:
            cls = primary[0]
            parts.append(f"=== CLASS: {cls['name']} (file: {cls['file']}) ===")
            for method in cls.get("methods", []):
                parts.append(self._format_func(method))
        elif primary:
            parts.append("=== PRIMARY CODE (directly relevant to the question) ===")
            for func in primary:
                parts.append(self._format_func(func))


        if dependencies:
            parts.append("\n=== DEPENDENCIES (functions called by the above) ===")
            parts.append("These are included so you understand what the parameters and called functions do.")
            for func in dependencies:
                parts.append(self._format_func(func))

        if callers:
            parts.append("\n=== CALLERS (functions that use the above) ===")
            parts.append("These show where and how the primary code is used in the broader codebase.")
            for func in callers:
                parts.append(self._format_func(func))

        if not parts:
            return "No relevant code found for this query."

        return "\n".join(parts)

    def _format_func(self, func):
        """Formats a single function dict into a readable block."""
        class_label = f" [method of {func['class']}]" if func.get("class") else ""
        param_label = ", ".join(func.get("params", []))
        calls_label = ", ".join(func.get("calls", [])) if func.get("calls") else "none"
        return (
            f"\n--- {func['name']}{class_label} ---\n"
            f"File      : {func.get('file', 'unknown')}\n"
            f"Parameters: {param_label}\n"
            f"Calls     : {calls_label}\n"
            f"Code:\n{func.get('code', '')}\n"
        )

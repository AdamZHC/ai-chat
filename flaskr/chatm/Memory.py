class MemoryUtil:
    MEMORY_KEY = "chat_history"
    MEMORY_FORMAT = "{chat_history}"
    @staticmethod
    def add_prefix_template(template):
        return "{}/n{}".format(MemoryUtil.MEMORY_FORMAT, template)


    @staticmethod
    def add_prefix_input_variables(input_variables):
        input_variables.append(MemoryUtil.MEMORY_KEY)
        return input_variables
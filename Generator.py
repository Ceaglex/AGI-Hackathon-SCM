from ErnieLLM import ErnieLLM

"""
这个部分的代码去写Generate部分，
可以

"""


class PromptGenerator:

    def __init__(self, model_series="ernie"):
        if model_series == "ernie":
            self.llm = ErnieLLM()
        else:
            # 这个部分是之后做LLM对比的时候改动的
            self.llm = ErnieLLM()

    def generate(self, input_prompt, strategy="zero-shot cot", examples=None):
        """
        :param shot:用户给出的样例，缺省时不可使用few-shot策略
        """
        if strategy == "zero-shot cot":
            zero_shot_cot_prompt = f"""
            你是一个优秀的prompt engineer，你擅长使用zero-shot cot策略改写prompt，最经典的zero-shot cot策略当然是在prompt里直接加上一句："Let's work on this problem step-by-step." 
            但我们需要针对当前任务去设计针对性的prompt，比如对于数学计算任务，输出的step就是运算的中间步骤和运算结构，last-step输出的答案是通过多个step的中间结果计算得到的。
            以下是你需要处理的origin-prompt，其中蕴含着当前任务的特征，你需要充分理解当前任务的特点设计step-by-step的zero-shot cot策略，但严禁直接给出答案。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，在最后返回你的zero-shot cot prompt，格式如下：
            {"{"}
                new_prompt: "你的zero-shot cot prompt",
            {"}"}
            """
            re_prompt = self.llm.response(zero_shot_cot_prompt)
            return re_prompt
        elif strategy == "few-shot cot":
            few_shot = []
            example_cot_prompt_template = """
            你是一个优秀的语言模型，你擅长用思维链的形式解释由问题到答案的推理过程，在你曾经的杰作中，
            对于input="(2/2+8*√2)^2 output:129 + 16*√2"
            你给出了如下的逻辑清晰的解决方案
            output="
            1. 2/2 = 1
            2. (2/2 + 8*√2)^2 = (1 + 8*√2)^2
            3. (1 + 8*√2)^2 = 1 + 16*√2 + 128
            4. 1 + 16*√2 + 128 = 129 + 16*√2
            所以最终结果是：129 + 16*√2"
            以下是你面临的新数据：{example}，其中已经给出问题和答案，但你需要补齐中间的推理过程
            """
            for example in examples:
                few_shot.append(self.llm.response(example_cot_prompt_template.format(example=example)))
            print(few_shot)
            few_shot_cot_prompt = f"""
            你是一个优秀的prompt engineer，你擅长使用few-shot cot策略改写prompt。最经典的few-shot cot策略当然是在prompt的末尾加上一句"Let's work on this problem step-by-step."，
            然后将所给的示例进行cot拆解，比如shot="input:(2/2+8*√2)^2 output:129 + 16*√2"，那么你需要在prompt的末尾cot拆解后的shot，对于所给的shot样例即：
            1. 2/2 = 1
            2. (2/2 + 8*√2)^2 = (1 + 8*√2)^2
            3. (1 + 8*√2)^2 = 1 + 16*√2 + 128
            4. 1 + 16*√2 + 128 = 129 + 16*√2
            所以最终结果是：129 + 16*√2"
            " 
            但我们需要针对当前任务去设计针对性的prompt，比如对于数学计算任务，输出的step就是运算的中间步骤和运算结构，last-step输出的答案是通过多个step的中间结果计算得到的。
            以下是与当前任务相关的few-shot示例，请你直接附在修改后的prompt里，千万不要完全遗漏掉few-shot示例，否则这不是一个完整的few-shot cot prompt而是zero-shot。
            few-shot:{few_shot}
            以下是你需要处理的origin-prompt，其中蕴含着当前任务的特征，你需要充分理解当前任务的特点设计step-by-step的few-shot cot策略，但千万不要直接给出答案。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，在最后返回你的few-shot cot prompt，格式如下：
            {"{"}
                new_prompt: "你的few-shot cot prompt" ,
            {"}"}
            """
            re_prompt = self.llm.response(few_shot_cot_prompt)
        elif strategy == "zero-shot contrastive":
            zero_shot_contrastive_prompt = f"""
            你是一个优秀的prompt engineer，你擅长使用zero-shot contrastive策略改写prompt，即给出在解决当前任务时比较容易犯下的错误
            比如对于数学计算任务，常见的错误就是忘记加上括号，比如"(2/2+8*√2)^2"，如果没有括号，那么就会变成"2/2+8*√2^2"，而这个结果是错误的。
            以下是你需要处理的origin-prompt，其中蕴含着当前任务的特征，你需要充分理解当前任务的特点设计step-by-step的few-shot cot策略，但千万不要直接给出答案。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，在最后返回你的few-shot contrastive prompt，格式如下：
            {"{"}
                new_prompt: "你的few-shot contrastive prompt" ,
            {"}"}
            """
            re_prompt = self.llm.response(zero_shot_contrastive_prompt)
        return re_prompt


if __name__ == "__main__":
    prompt_generator = PromptGenerator()
    # print(prompt_generator.generate("如果我和我名义上的妈妈没有血缘关系，那么我妈妈有没有可能不是我外婆的女儿？", "few-shot cot"))
    examples = ["input:求直角边长度分别为3和4的直角三角形的面积 output:6"]
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "zero-shot cot"))
    print(prompt_generator.generate("鸡兔同笼，头共35个，脚共104只，求鸡与兔各有多少个头？", "few-shot cot",
                                    examples=examples))

# import requests, uuid
# from googletrans import Translator,models
# from googletrans import urls, utils
#  # from googletrans.compat import PY3
# from googletrans.constants import DEFAULT_USER_AGENT
# subscription_key = '32f1cb9c935a4cd4b33825e2869bff0f'
#
# class MyTranslator(Translator):
#     def __init__(self,service_urls=None, user_agent=DEFAULT_USER_AGENT,
#                  proxies=None, timeout=None):
#         super().__init__(service_urls,user_agent,proxies,timeout)
#
#     def _translate(self, text, dest, src):
#         # if not PY3 and isinstance(text, str):  # pragma: nocover
#         #     text = text.decode('utf-8')
#         #     print(text)
#
#         token = self.token_acquirer.do(text)
#         params = utils.build_params(query=text, src=src, dest=dest,
#                                     token=token)
#         params['client'] = 'webapp'
#         url = urls.TRANSLATE.format(host=self._pick_service_url())
#         r = self.session.get(url, params=params)
#
#         data = utils.format_json(r.text)
#         return data
#
# def get_extra_result_of_single_word(word, translator):
#     """
#
#     :param word: single word string contain no space
#     :param translator: google translator object
#     :return: result string
#     """
#     translate_res = translator.translate(word, dest='zh-cn')
#     extra_data = translate_res.extra_data
#     all_translations_list = extra_data['all-translations']
#     result = ''
#     if all_translations_list is None:
#         result = translate_res.text
#         pass
#     else:
#         for translation in all_translations_list:
#             word_class = translation[0]
#             result += word_class + '\n    '
#             word_tsl_list = translation[2]
#             for tsl in word_tsl_list:
#                 tsl_res = tsl[0]
#                 tsl_src_list = tsl[1]
#                 tsl_src = ''
#                 # obj = ''
#                 # confidence = 0
#                 if tsl_src_list is None:
#                     pass
#                 else:
#                     for i in tsl_src_list:
#                         tsl_src += i + ' '
#                 # if len(tsl) <3:
#                 #     pass
#                 # else:
#                 #     obj = tsl[2]
#                 #     confidence = tsl[3]
#                 result += '{0} [{1}]\n    '.format(tsl_res, tsl_src)
#             result += '\n'
#     return result
#
#     pass
#
# def get_translation_by_google(text_input):
#     translator = MyTranslator(service_urls=["translate.google.cn"])
#     if len(text_input.split()) == 1:
#         trans_result = get_extra_result_of_single_word(text_input.split()[0], translator)
#     else:
#         trans_result = translator.translate(text_input, dest='zh-cn').text
#     return trans_result
#
# def get_translation(text_input, language_output="zh-Hans"):
#     if not text_input:
#         return ""
#
#     base_url = 'https://api.cognitive.microsofttranslator.com'
#     path = '/translate?api-version=3.0'
#     params = '&to=' + language_output
#     constructed_url = base_url + path + params
#
#     headers = {
#         'Ocp-Apim-Subscription-Key': subscription_key,
#         'Ocp-Apim-Subscription-Region': 'global',
#         'Content-type': 'application/json',
#         'X-ClientTraceId': str(uuid.uuid4())
#     }
#
#     body = [{
#         'text' : text_input
#     }]
#     response = requests.post(constructed_url, headers=headers, json=body)
#     result = response.json()
#     return result[0]['translations'][0]['text']
import os
from openai import OpenAI


class Translator:
    def getTranslate(self, text):
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("The DASHSCOPE_API_KEY environment variable is not set.")

        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        try:
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {'role': 'system', 'content': '你是一个翻译员，我会给你提供单个单词，词组或文段；针对单词和词组首先要进行解释，对不同的意思分别用对应语言组句，对长篇文段直接翻译。回答尽可能精炼节省token'},
                    {'role': 'user', 'content': text}
                ]
            )
            return (completion.choices[0].message.content)
        except Exception as e:
            print(f"An error occurred: {e}")


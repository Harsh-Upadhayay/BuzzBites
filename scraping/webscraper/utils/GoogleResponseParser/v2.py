import re
import json
import jsbeautifier
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
from slimit.parser import Parser
from .base import GoogleSearchResponseParserBase

class GoogleSearchResponseParserV2(GoogleSearchResponseParserBase):
    def __init__(self):
        self.js_parser = Parser()

    def ext_funs(self, js_code):
        pattern = r'\(function\(\) \{\s*([\s\S]*?)\s*\}\);?'
        matches = re.findall(pattern, js_code)
        function_list = []
        for match in matches:
            function_list.append(match)
        function_list.sort(key=len, reverse=True)
        return function_list

    def ext_scripts(self, response):
        script_tags = response.xpath('//script')
        script_tags = sorted(script_tags, key=lambda tag: len(str(tag)))
        beautified_js_list = []
        for tag in script_tags:
            beautified_js_list.append(jsbeautifier.beautify(str(tag)))
        beautified_js_list.sort(key=len, reverse=True)
        return beautified_js_list

    def ext_vars(self, js_code):
        variables = {}
        try:
            tree = self.js_parser.parse(js_code)
            for node in nodevisitor.visit(tree):
                if isinstance(node, ast.VarStatement):
                    for var_decl in node.children():
                        if isinstance(var_decl, ast.VarDecl):
                            variables[var_decl.identifier.value] = var_decl.initializer.to_ecma()
        except:
            pass
        return variables

    def ext_url(self, cp_value):
        
        try:
            if 'http' in cp_value[1][3][0]:
                return cp_value[1][3][0]
            else:
                return None
        except:
            return None

    def ext_urls(self, m_value):
        urls = []
        try:
            x = json.loads(m_value)
            for key, cp_value in x.items():       
                if(url := self.ext_url(cp_value)):
                    urls.append(url)
        except:
            pass
        return urls

    def image_sources(self, response, early_exit=False):

        scripts = self.ext_scripts(response)
        urls = []
        for script in scripts:
            functions = self.ext_funs(script)
            for function in functions:
                variables = self.ext_vars(function)
                for key, m_value in variables.items():
                    urls.extend(self.ext_urls(m_value))

            if early_exit and urls:
                break
    
        return urls


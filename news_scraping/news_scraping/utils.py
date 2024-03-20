class TextHandler:

    def _filter_text(self, text):
        if isinstance(text, list):
            if len(text) > 0:	
                return self._filter_text((' ').join(text))
            return None
        else:
            if text == None:
                return None
            else:
                text = text.replace(u'\\n', u' ')
                text = text.replace(u'<br>', u' ')
                text = ' '.join(text.split())
			# return ''.join(text).strip()
        return text
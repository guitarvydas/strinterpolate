all: install
	pbp/t2t.bash . ./pbp string.ohm string.rwr empty.js mad.si >mad.py
	@echo
	@echo '*** generated code ***'
	@cat mad.py
	@echo
	@echo '*** run ***'
	@python3 mad.py

identity:
	pbp/t2t.bash . ./pbp string.ohm identity-string.rwr empty.js mad.si

install:
	npm install


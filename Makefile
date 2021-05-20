.PHONY: local deploy build
StarvanityContactFlow ?= StarvanityContactFlow

local:
	npm run build 
	sam local invoke generateVanityNoA4C8436B --event test/event.json
build:
	npm run build
	cdk synth

deploy:
	npm install
	npm run build 
	cdk bootstrap
	cdk deploy --parameters connectInstanceArn=${connectInstanceArn} --parameters contactFlowName=$(StarvanityContactFlow)



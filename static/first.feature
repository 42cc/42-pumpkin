Feature: First Example Feature
	In order to get show you what is pumpkin
	As it`s developer
	I want to give you some example4

	Scenario: Give pumpkin some file to process
		Given I Have pumpkin app
		And i have some testing utils
		When I give it a file named first.ftrs
		Then I Should see succesfull output
		And Everything should be fine

	Scenario: Some second scenario
		Given I Have pumpkin 
		And i have some testing utils
		When I give it a file named first.ftrs
		Then I Should do nothing

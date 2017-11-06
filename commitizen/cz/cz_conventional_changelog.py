import os
from commitizen.cz.cz_base import BaseCommitizen
import re
import textwrap

__all__ = ['ConventionalChangelogCz']


class ConventionalChangelogCz(BaseCommitizen):
    def questions(self):
        questions = [
            {
                'type': 'list',
                'name': 'prefix',
                'message': 'Select the type of change you are committing',
                'choices': [
                    {
                        'value': 'feat',
                        'name': 'feat: A new feature',
                    },
                    {
                        'value': 'fix',
                        'name': 'fix: A bug fix',
                    },
                    {
                        'value': 'docs',
                        'name': 'docs: Documentation only changes',
                    },
                    {
                        'value': 'style',
                        'name': ('style: Changes that do not affect the '
                                 'meaning of the code (white-space, formatting,'
                                 ' missing semi-colons, etc)'),
                    },
                    {
                        'value': 'refactor',
                        'name': ('refactor: A code change that neither fixes '
                                 'a bug nor adds a feature')
                    },
                    {
                        'value': 'perf',
                        'name': 'perf: A code change that improves performance',
                    },
                    {
                        'value': 'test',
                        'name': ('test: Adding missing or correcting '
                                 'existing tests')
                    },
                    {
                        'value': 'chore',
                        'name': ('chore: Changes to the build process or '
                                 'auxiliary tools and libraries such as '
                                 'documentation generation'),
                    },
                ]
            },
            {
                'type': 'input',
                'name': 'scope',
                'message': ('What is the scope of this change (e.g. component or file name)? (press enter to skip)\n')
            },
            {
                'type': 'input',
                'name': 'subject',
                'message': ('Write a short, imperative tense description of the change:\n')
            },
            {
                'type': 'input',
                'name': 'body',
                'message': ('Provide a longer description of the change: (press enter to skip)\n')
            },
            {
                'type': 'confirm',
                'name': 'isBreaking',
                'message': 'Are there any breaking changes?',
                'default': False
            },
            {
                "type": "input",
                "name": "breaking",
                "message": "Describe the breaking changes:\n",
                "when": self.is_breaking_answers
            },
            {
                "type": 'confirm',
                "name": 'isIssueAffected',
                "message": 'Does this change affect any open issues?',
                "default": False
            },
            {
                "type": 'input',
                "name": 'issues',
                "message": 'Add issue refere nces (e.g. "fix #123", "re #123".):\n',
                "when": self.is_issued_affected
            }
        ]
        return questions

    def message(self, answers):
        wrapper = textwrap.TextWrapper(width=100)
        prefix = answers['prefix']
        scope = answers['scope']
        issues = ' '.join(wrapper.wrap(answers.get('issues'))) if 'issues' in answers else ''
        subject = answers['subject']
        body = answers['body']
        # footer = answers['footer']
        breaking = answers['breaking'] if 'breaking' in answers else ''
        if len(breaking) > 0:
            breaking = 'BREAKING CHANGE: ' + re.sub(r'/^BREAKING CHANGE: /', '', breaking)
        breaking = ' '.join(wrapper.wrap(breaking))
        # breaking = wrapper.fill(breaking)
        footer = '{}\n\n'.format(breaking)
        message = ''

        if prefix:
            message += '{0}'.format(prefix)
            if scope:
                message += '({0})'.format(scope)
            message += ': '
        if issues:
            message += '{} '.format(issues)
        if subject:
            message += '{0}'.format(subject)
        if body:
            message += '\n\n{0}'.format(body)
        if footer:
            message += '\n\n{0}'.format(footer)
        print message
        return message

    def example(self):
        return (
            'feat($injector): ability to load new modules after bootstrapping\n'
            '\nThe new method `$injector.loadNewModules(modules)` will add '
            'each of the\ninjectables to the injector and execute all of the '
            'config and run blocks\nfor each module passed to the method.\n'
            '\nCloses #324'
        )

    def schema(self):
        return ('<type>(<scope>): <subject>\n'
                '<BLANK LINE>\n'
                '<body>\n'
                '<BLANK LINE>\n'
                '<footer>')

    def info(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, 'cz_conventional_changelog_info.txt')
        with open(filepath, 'r') as f:
            content = f.read()
        return content

    def is_breaking_answers(self, answers):
        return answers.get('isBreaking')

    def is_issued_affected(self, answers):
        return answers.get('isIssueAffected')

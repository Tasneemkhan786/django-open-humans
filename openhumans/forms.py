from django import forms


class MessageProjectMembersForm(forms.Form):
    """A form for validating messages and emailing the members of a project."""

    access_token = forms.CharField(
        label='Master access token',
        help_text='link to master acces token',
        required=False)

    all_members = forms.BooleanField(
        label='Message all project members?',
        required=False)

    project_member_ids = forms.CharField(
        label='Project member IDs',
        help_text='A comma-separated list of project member IDs.',
        required=False,
        widget=forms.Textarea)

    subject = forms.CharField(
        label='Message subject',
        help_text='''A prefix is added to create the outgoing email subject.
        e.g. "[Open Humans Project Message] Your subject here"''',
        required=False)

    message = forms.CharField(
        label='Message text',
        help_text="""The text of the message to send to each project member
        specified above. You may use <code>{{ PROJECT_MEMBER_ID }}</code> in
        your message text and it will be replaced with the project member ID in
        the message sent to the member.""",
        required=True,
        widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(MessageProjectMembersForm, self).clean()
        all_members = cleaned_data.get("all_members")
        project_member_ids = cleaned_data.get("project_member_ids")
        access_token = cleaned_data.get("access_token")
        if all_members and project_member_ids:
            raise forms.ValidationError('Either all members should be ' +
                                        'selected or project member ids ' +
                                        'should be provided, not both.')
        if access_token:
            project_member_ids = project_member_ids.split(',')
            project_member_ids = [pmi.strip() for pmi in project_member_ids
                                  if pmi.strip()]
            self.cleaned_data['project_member_ids'] = project_member_ids
            for project_member_id in project_member_ids:
                if not project_member_id.isdigit():
                    raise forms.ValidationError('Project member id must ' +
                                                'be a number')
                if len(project_member_id) != 8:
                    raise forms.ValidationError('Project member id must ' +
                                                'be eight digits long')

            if not all_members and not project_member_ids:
                raise forms.ValidationError('Either all members should be ' +
                                            'selected or project member ids ' +
                                            'should be provided')

        return cleaned_data

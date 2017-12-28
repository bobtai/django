from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label='請輸入一個IM客服問題', max_length=100, initial='')
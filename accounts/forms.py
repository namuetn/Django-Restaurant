from django import forms
from accounts.models import User


class UserForm(forms.ModelForm):
    # widget: se chi ra giao dien cua o input default cua django
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    '''
    Clean()
    Trong Django, clean() là một phương thức đặc biệt được sử dụng trong lớp form để thực hiện kiểm tra và xử lý dữ liệu 
    đầu vào của form. Phương thức này được gọi sau khi người dùng đã gửi dữ liệu từ trình duyệt và trước khi dữ liệu 
    được lưu vào cơ sở dữ liệu. Mục đích chính của clean() là kiểm tra tính hợp lệ của dữ liệu và làm sạch dữ liệu nếu cần.
    '''
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")
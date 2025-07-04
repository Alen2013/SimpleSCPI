using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace SimpleSCPI.UI.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        [ObservableProperty]
        private string title = "Hello MVVM Toolkit";

        [RelayCommand]
        private void ShowMessage()
        {
            Title = "按钮已点击！";
        }
    }
} 
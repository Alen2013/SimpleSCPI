using System.Configuration;
using System.Data;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using SimpleSCPI.UI.ViewModels;

namespace SimpleSCPI.UI;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    public static IHost AppHost { get; private set; }

    public App()
    {
        AppHost = Host.CreateDefaultBuilder()
            .ConfigureServices((context, services) =>
            {
                services.AddSingleton<MainViewModel>();
                services.AddSingleton<MainWindow>();
            })
            .Build();
    }

    protected override async void OnStartup(StartupEventArgs e)
    {
        await AppHost.StartAsync();
        var mainWindow = AppHost.Services.GetRequiredService<MainWindow>();
        mainWindow.Show();
        base.OnStartup(e);
    }

    protected override async void OnExit(ExitEventArgs e)
    {
        await AppHost.StopAsync();
        AppHost.Dispose();
        base.OnExit(e);
    }
}


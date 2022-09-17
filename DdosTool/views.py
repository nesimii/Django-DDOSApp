# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from DdosTool.forms import LoginUserForm, CommandForm, DeviceForm
from DdosTool.models import Devices, Commands
from DdosTool.ssh.devices import SshProc

devices = SshProc()


def loginRequest(request):
    if request.user.is_authenticated:
        return redirect('commands')

    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                nextUrl = request.GET.get('next', None)
                if nextUrl is None:
                    return redirect("commands")
                else:
                    return redirect(nextUrl)
            else:
                return render(request, 'login.html', context={'form': form})
        else:
            return render(request, 'login.html', context={'form': form})
    else:
        form = LoginUserForm()
        return render(request, 'login.html', context={'form': form})


def logoutRequest(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def commandList(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CommandForm()
    komutlar = Commands.objects.all()

    return render(request, 'command_list.html', context={'form': form, 'commands': komutlar})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def editCommand(request, pk):
    komut = get_object_or_404(Commands, pk=pk)
    if request.method == 'POST':
        form = CommandForm(request.POST, instance=komut)
        if form.is_valid():
            form.save()
            return redirect('commandList')
    else:
        form = CommandForm(instance=komut)
    return render(request, 'editCommand.html', context={'form': form})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def deleteCommand(request, pk):
    if Commands.objects.filter(pk=pk).exists():
        Commands.objects.filter(pk=pk).delete()
    return redirect('commandList')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def deviceList(request):
    dev = Devices.objects.all()
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            if validate_ip_address(form.cleaned_data["ip"]) is False:
                return render(request, 'device_list.html',
                              context={'form': form, 'devices': dev, 'error': 'ip adresini kontrol edin'})
            if Devices.objects.filter(ip=form.cleaned_data["ip"]).exists():
                return render(request, 'device_list.html',
                              context={'form': form, 'devices': dev, 'error': 'ip adresi kayıtlı'})

            d = Devices(ip=form.cleaned_data["ip"], username=form.cleaned_data["username"],
                        password=form.cleaned_data['password'])
            d.save()
    else:
        form = DeviceForm()

    return render(request, 'device_list.html', context={'form': form, 'devices': dev})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def editDevice(request, pk):
    device = get_object_or_404(Devices, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('deviceList')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'editDevice.html', context={'form': form})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def deleteDevice(request, pk):
    if Devices.objects.filter(pk=pk).exists():
        Devices.objects.filter(pk=pk).delete()
    return redirect('deviceList')


@login_required(login_url='login')
def commands(request):
    commandListe = Commands.objects.all()
    dev = Devices.objects.all()
    return render(request, 'commands.html', context={'commands': commandListe, 'devices': dev})


# ajav post istekleri için
@user_passes_test(lambda u: u.is_superuser)
def sshCommands(request):
    if request.method == "GET":
        return JsonResponse({'error': 'GET isteği alındı'}, status=200)

    if request.method == 'POST':
        post = request.POST

        if post.get('text') == 'sendCommand':
            commandId = post.get('commandId')
            print('komut id: ', commandId)
            targetIp = post.get('targetIp')
            if validate_ip_address(targetIp) is False:
                return JsonResponse({'error': 'ip adresini kontrol edin'}, status=200)
            if Commands.objects.filter(pk=commandId).exists() is False:
                return JsonResponse({'error': 'komut id si hatalı'}, status=200)

            command = Commands.objects.get(pk=commandId)
            if 'install' in command.commandText:
                text = command.commandText
            elif 'apt' in command.commandText:
                text = command.commandText
            elif 'update' in command.commandText:
                text = command.commandText
            else:
                text = command.commandText + " " + targetIp
            print('oluşturulan text: ', text)
            print('bant genişliği: ', command.bandwidth)
            if devices.sendCommand(command=text, bandwidth=command.bandwidth):
                return JsonResponse({'text': 'Komut Çalıştırılıyor'}, status=200)
            else:
                return JsonResponse({'error': 'komutlar gönderilemedi, aktif işlem durumunu kontrol edin'}, status=200)

        elif post.get('text') == 'cancelCommand':
            if devices.cancelCommand():
                return JsonResponse({'text': 'process&thread kapatıldı'}, status=200)
            else:
                return JsonResponse({'error': 'process&thread kapatılamadı, aktif işlem olmadığından emin olun'},
                                    status=200)

    return JsonResponse({'text': 'error'}, status=200)


def validate_ip_address(address):
    try:
        parts = address.split(".")

        if len(parts) != 4:
            print("IP address {} is not valid".format(address))
            return False

        for part in parts:
            if not isinstance(int(part), int):
                print("IP address {} is not valid".format(address))
                return False

            if int(part) < 0 or int(part) > 255:
                print("IP address {} is not valid".format(address))
                return False

        print("IP address {} is valid".format(address))
        return True
    except:
        return False

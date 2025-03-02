# bbFuzzing.txt

**bbFuzzing.txt** is a unique wordlist that is 90% generated with OpenAI ChatGPT. 

Below are links to tools that allow you to bypass 401/403 status code. 

Tools for 403/401 bypass
1. [bypassfuzzer](https://github.com/intrudir/BypassFuzzer) by @intrudir
2. [bypass-url-parser](https://github.com/laluka/bypass-url-parser) by @TheLaluka
3. [dontgo403](https://github.com/devploit/dontgo403) by @devploit
4. [nomore403](https://github.com/devploit/nomore403) by @devploit

There are also examples of how you can extend the fuzzing process to get more interesting results (proxy level misconfigurations, temporary files, etc.).

# Ffuf (my approach to minimizing fp)
- **fp_domains.txt** - list of domains that give too much false positives, check them separately with ffuf filters
- **fuzz_output.txt** - can work with results
```
ffuf -u URL/TOP -w domains.txt:URL -w top.txt:TOP -ac -mc 200 -o fuzz_results.json -fs 0
python delete_falsepositives.py -j fuzz_results.json -o fuzz_output.txt -fp fp_domains.txt
```
# Ffuf
```
> ffuf -u target.com/FUZZ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ -H "Host: 127.0.0.1" -w bbFuzzing.txt
> ffuf -u target.com/FUZZ -H "Host: localhost" -w bbFuzzing.txt

> ffuf -u target.com/FUZZ.example -w bbFuzzing.txt
> ffuf -u target.com/FUZZ.sample -w bbFuzzing.txt
> ffuf -u target.com/FUZZ.template -w bbFuzzing.txt

> ffuf -u target.com/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/%3B/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/..%3B/FUZZ/ -w bbFuzzing.txt

> ffuf -u target.com/FUZZ..%2f -w bbFuzzing.txt
> ffuf -u target.com/FUZZ%09 -w bbFuzzing.txt
> ffuf -u target.com/FUZZ%23 -w bbFuzzing.txt

> ffuf -u target.com/FUZZ..%00 -w bbFuzzing.txt
> ffuf -u target.com/FUZZ;%09 -w bbFuzzing.txt
> ffuf -u target.com/FUZZ;%09.. -w bbFuzzing.txt

> ffuf -u target.com/FUZZ;%09..; -w bbFuzzing.txt
> ffuf -u target.com/FUZZ;%2f.. -w bbFuzzing.txt
> ffuf -u target.com/.FUZZ -w bbFuzzing.txt

> ffuf -u target.com/%0AFUZZ -w bbFuzzing.txt
> ffuf -u target.com/%0D%0AFUZZ -w bbFuzzing.txt
> ffuf -u target.com/%0DFUZZ -w bbFuzzing.txt

> ffuf -u target.com/%2e/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ%20 -w bbFuzzing.txt
> ffuf -u target.com/FUZZ%2520 -w bbFuzzing.txt

> ffuf -u target.com/%u002e%u002e/%u002e%u002e/FUZZ -w bbFuzzing.txt
> ffuf -u target.com/%2e%2e%2f/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/%2EFUZZ -w bbFuzzing.txt

> ffuf -u target.com/FUZZ.old -w bbFuzzing.txt
> ffuf -u target.com/FUZZ?.css -w fuzzing.txt
> ffuf -u target.com/FUZZ?.js -w fuzzing.txt

> ffuf -u target.com/_FUZZ -w bbFuzzing.tx
> ffuf -u target.com/FUZZ_ -w bbFuzzing.txt
> ffuf -u target.com/_FUZZ_ -w bbFuzzing.txt

> ffuf -u target.com/..;/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/..;/..;/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/../FUZZ -w bbFuzzing.txt

> ffuf -u target.com/-FUZZ -w bbFuzzing.txt
> ffuf -u target.com/~FUZZ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ..;/ -w bbFuzzing.txt

> ffuf -u target.com/FUZZ;/ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ# -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/~ -w bbFuzzing.txt

> ffuf -u target.com/!FUZZ -w bbFuzzing.txt
> ffuf -u target.com/#/FUZZ/ -w bbFuzzing.txt
> ffuf -u target.com/-/FUZZ/ -w bbFuzzing.txt

> ffuf -u target.com/FUZZ~ -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/.git/config -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/.env -w bbFuzzing.txt

> ffuf -u target.com/FUZZ. -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/* -w bbFuzzing.txt
> ffuf -u target.com/FUZZ/? -w bbFuzzing.txt

> ffuf -u target.com/FUZZ -recursive -w fuzzing.txt
> ffuf -u target.com/FUZZ -recursive -w fuzzing.txt -e .asp,.aspx,.ashx,.ash,.jsp,.jspx,.php,.js,.dll,.json,.bak,.bkp,.conf,.txt,.py,.zip,.tar.gz,.tar,.7z,.old

Any special occasions (cookieless) - IIS + ASP
> ffuf -u target.com/(A(ABCD))/FUZZ
> ffuf -u target.com/(ABCD)/FUZZ
> ffuf -u target.com/(A(XXXXXXXX)F(YYYYYYYY))/FUZZ
> ffuf -u target.com/FUZZ/(S(X))/
> ffuf -u target.com/bin::$INDEX_ALLOCATION/FUZZ
> ffuf -u target.com/bin::$INDEX_ALLOCATION/FUZZ.dll
> ffuf -u target.com/bin::$INDEX_ALLOCATION/FUZZ -e .asp,.aspx,.ashx,.ash,.dll
```
5. [pathbuster](https://github.com/ethicalhackingplayground/pathbuster) by @ethicalhackingplayground
```
> pathbuster --urls crawls.txt --payloads traversals.txt --wordlist wordlist.txt -o output.txt
```
![image](https://github.com/reewardius/bbFuzzing.txt/assets/68978608/538999ff-3bac-4291-a347-e701cc1f21d5)
![image](https://github.com/reewardius/bbFuzzing.txt/assets/68978608/88c5c7d7-93e5-471e-8806-9c565207d3fa)

6. [TProxer](https://github.com/ethicalhackingplayground/TProxer) - Burp Suite extension made to automate the process of finding reverse proxy path based SSRF by @ethicalhackingplayground

![image](https://github.com/reewardius/bbFuzzing.txt/assets/68978608/be1496fe-8cc2-4494-867d-dcb46a13b113)
![image](https://github.com/reewardius/bbFuzzing.txt/assets/68978608/5df4ce2b-644b-4ed2-a9d9-1c4112f59a91)

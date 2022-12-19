# Setup von Docker unter Windows ohne Docker Desktop

!!! note
    Diese Anleitung basiert auf einem sehr ausführlichen Blog Artikel, der ein komplexeres Setup (mehrere Linux Distros parallel) beschreibt.
    Der Artikel ist hier zu finden <https://dev.to/bowmanjd/install-docker-on-windows-wsl-without-docker-desktop-34m9>

!!! important
    Voraussetzung für diese Anleitung ist eine funktionierende WSL2 Installation. Eine Anleitung dazu befindet sich [hier](wsl2_setup_fhhnet.md).

In dieser Anleitung wird beschrieben, wie man:

* Docker in Ubuntu installiert
* `docker-compose` installiert
* den DockerDaemon startet (`dockerd`)

Nach durcharbeiten dieser Anleitung kann Docker auf einem FHHNET-Rechner benutzt werden.
Am Ende dieser Anleitung sind die einzelnen Schritte noch mal in einem [Skript](#all-in-one-setup-script) zusammengefasst. Dies erspart die Eingabe der einzelnen Schritte.

## Installation von Docker

### Vorarbeiten

Zunächst sollte alle bisherigen Pakete auf den neuesten Stand gebracht werden

```bash
sudo apt update && sudo apt upgrade
```

Wenn zuvor schon mit Docker herum experimentiert wurde sollten alle Pakete gelöscht werden.

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

Sicherstellen, dass benötigte Pakete installiert sind

```bash
sudo apt install --no-install-recommends apt-transport-https ca-certificates curl gnupg2
```


### Docker package repository hinzufügen


Infos über das Betriebssystem in Umgebungsvariablen laden:
```bash
source /etc/os-release
```


Das offizielle Docker Repo als vertrauenswürdige Quelle hinzufügen:
```bash
curl -fsSL https://download.docker.com/linux/${ID}/gpg | sudo apt-key add -
```

und in die `sources.list` eintragen und die Paketquellen aktualisieren:
```bash
echo "deb [arch=amd64] https://download.docker.com/linux/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
```

### Docker tatsächlich installieren
```bash
sudo apt install docker-ce docker-ce-cli containerd.io
```


### `docker-compose` installieren

Aus der offiziellen Anleitung [hier](https://docs.docker.com/compose/install/).

!!! Note
    Erweiterung ggü. der offiziellen Anleitung:
    `sudo` benötigt den Parameter `-E` damit die Umgebungsvariablen des normalen Users übernommen werden (Proxy settings)

```bash
sudo -E curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Jetzt muss die Datei noch ausführbar gemacht werden.

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

### Den eigenen Benutzer zur Gruppe `docker` hinzufügen

```bash
sudo usermod -aG docker $USER
```

und Gruppen neu laden

```bash
newgrp docker
```

<!-- !!! attention
    WSL Terminal schließen und neu öffnen, damit Änderungen wirksam werden -->


Die Ausgabe von
```bash
groups
```

sollte nun `docker` beinhalten.

## `dockerd` Starten und testen

### Starten

`sudo service docker start` \ \ \ [`stop`] [`restart`] [`status`]

### Testen
```bash
docker run --rm hello-world
```



## All in one setup script

```bash
#!bin/bash
sudo apt update && sudo apt upgrade
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt install --no-install-recommends apt-transport-https ca-certificates curl gnupg2
source /etc/os-release
curl -fsSL https://download.docker.com/linux/${ID}/gpg | sudo apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo -E curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker $USER
newgrp docker 
sudo tee -a /etc/default/docker.auto <<EOF 
EOF

```




<!-- ### `dockerd` ohne Passwort starten (optional)

`dockerd` ist ein Daemon und kann somit nur mit Rootrechten gestartet werden. Wenn gewünscht ist dass `dockerd` automatisch startet ist das ggf. unerwünscht, da die Eingabe des Passworts nötig ist.
Man kann dieses Problem umgehen, indem man der Gruppe `docker` die Ausführung auch als Nicht-Root-User erlaubt. Dazu muss der Befehl `sudo visudo` ausgeführt werden. In dem sich öffnenden Editor müssen dann die folgende Zeile hinzugefügt werden.

```
# Allow members of the docker group to execute dockerd whithout password
%docker ALL=(ALL)  NOPASSWD: /usr/bin/dockerd
```

### `dockerd` automatisch starten (optional, nicht unbedingt zu empfehlen)

Wenn die automatische Ausführung von `dockerd` erwünscht ist, dann kann man folgende Zeile zur `~/.bashrc` hinzufügen.

```
# automatic lauch of dockerd
nohup sudo -b dockerd < /dev/null > ~/dockerd.log 2>&1
``` -->


# AI_Devs 2

Hey! This is repository for my course of AI_Devs 2.

## How to run

Fill `.env` file.

Install:

```sh
docker compose up -d
```

Jump into image shell:

```sh
docker exec -it ai_devs-2-app-1 bash
```

Then:

```sh
python main.py
```

Or in one line:

```sh
docker exec ai_devs-2-app-1 python main.py
```

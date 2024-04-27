 
  <h1 align="center">🦜️🔗 landau_research_bot🦜️🔗</h1>

---

<div align="center">
  <img src="assets/landau.jpg" height="400" width="400">
</div>

<div align="center">
наконец-то появился бот, который поможет вам в написании научной работы</div>


---

# Tech stack: 
<div>
  <img src="assets/gigachain.png" height="50" width="50">

  <img src="assets/python.jpg" height="50" width="50">

  <img src="assets/resend-header.webp" height="50" width="50">

  <img src="assets/peewee3-logo.png" height="50" width="100">

  <img src="assets/docker.png" height="50" width="150">

  <img src="assets/bash.png" height="50" width="50">
  <img src="assets/posty.png" height="50" width="50">
  <img src="assets/16178365.png" height="50" width="50">



</div>


# Использование 🛠️ 



Нажмите `/start` чтобы запустить бота

Нажмите `/help` чтобы получить помочь

напишите `end`, чтобы перейти в главное меню!

напишите `summarize`: и Отправьте научную работу который хочешь суммизировать! Также получи аудио суммари

напишите `brainstorm`: 
чтобы найти научную работу на любую тему, добавьте там почту в формате `email:user@example.com`, и чтобы получить резулать на почту отправьте запрос в формате: `mail:запрос`, а если не хотите получить резулать на почту отправьте запрос в формате: `nml:запрос`

напишите `assistant`:и спрашивайте бота обо всем на свете
,

Бот сохраняет состояния между разговорами, чтобы перейти в новый режим напишите `end`


# Установка ⚙️



## Первые шаги (docker-compose) 🚀


* Клонируйте проект, выполнив следующую команду:

    `git@github.com:shuklarituparn/landau_research_bot.git`
    

* Теперь выполните следующую команду, чтобы убедиться, что вы находитесь в корневой директории проекта:

    `cd landau_research_bot`



* Заполните файл `.env.example` в папке `bot` и переименуйте его в `.env`


* Заполните следующее в файле docker compose

*    > `POSTGRES_USER: <Юзернэм вашего постгреса>` 

*    > `POSTGRES_PASSWORD: <Пароль вашего постгреса>`

*    >  `POSTGRES_DB: <Название ваши базы данных>`
     


* Находясь в в корневой директории проекта, выполните следующую команду, чтобы запустить: `docker compose up`

> Убедитесь, что у вас установлен Docker перед выполнением вышеуказанной команды





---



## ENV Файл 📝


`BOT_TOKEN=<ваш бот-токен от @botfather>`

`TALLY_AI_TOKEN=<ваш токен>`


`SPEECH_SCOPE=<SALUTE_SPEECH_PERS>`

`SPEECH_CLIENT_ID=<ваш client_id>`

`SPEECH_CLIENT_SECRET=<ваш секрет>`

`SPEECH-AUTH-DATA=<auth_data>`

`GIGACHAT_CLIENT_ID=<client_id gigahcat>`

`GIGACHAT_SCOPE=GIGACHAT_API_PERS`

`DATABASE_NAME=<telegrambotuserdata>`

`DATABASE_USERNAME=<юзернейм>`

`DATABASE_PASSWORD=<пароль>`

`GIGACHAT_API_AUTH=<gigachat auth_data>`

Как получить токен доступа gigachain и salute-speech вы можете прочитать тут: (https://developers.sber.ru/docs/)


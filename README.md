# innopolis_final

Скрипт "Планировщик задач". Реализован на Python с использованием фреймворка Django.

В браузере открывать по адресу ../task

В качастве Users используется зарегистрированные пользователи Django. 
Форма регистрации пользователей отдельно не реализовывалась. Для создания новых пользователей рекомендуется использовать ../admin

Для корректной работы скрипта, в админке Django должны быть созданы 2 группы пользователей "Заказчики" и "Исполнители". Пользователь может быть и тем и другим одновременно. Передача пользователю админских прав осуществляется посредством "Staff status"

Николаев С.С.

# 2020-1-Atom-QA-Python-A-Kondakov
# Проект по тестированию веб -приложения
# Мануал к запуску проекта
#### Исходники  в  репозитории https://github.com/bimboterminator/course_project
#### 1. Создать  в докере кастомную сеть с названием my-network 
#### 2. Дженкинс должен быть собран с питоном  на борту, если его нет можно собрать из Dockerfile в диркетории на уровне с папками Project/code u Project/tmp. Также необходим плагин с Allure
##### Селеноид использует браузер vnc_chrome:87.0
#### 3. Собрать VK MOCK из докер файла, лежащего в директори Project/code
#### 4. Запустить Дженкинс командой:
* docker run -d  -v `<YOUR jenkins_home DIR>`:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker-compose):/usr/local/bin/docker-compose -e WD=`<ABSOLUTE PATH TO Project/ where code and tmp folders are>` --net host  jenkins

#### 5. Сбилдить джобу из файла test_qa.yaml в директории Project/tmp/jjb (со своим jenkins.ini разумеется)
#### Все приготовления совершены

#### Отчет по тестированию в файле report.md

### Пример работы дженкинса
![image_2021-03-05_15-47-10](https://user-images.githubusercontent.com/53858094/110122658-f27ed500-7dd0-11eb-9a05-f527c4519bb3.png)
![image_2021-03-05_15-47-41](https://user-images.githubusercontent.com/53858094/110122664-f4489880-7dd0-11eb-95a9-bfa6652555f7.png)
![image_2021-03-05_15-51-08](https://user-images.githubusercontent.com/53858094/110122748-0d514980-7dd1-11eb-9f83-747c9b57ad9a.png)

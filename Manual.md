#Мануал к запуску проекта

### 1. Создать  в докере кастомную сеть с названием my-network 
### 2. Дженкинс должен быть собран с питоном  на борту, если его нет можно собрать из Dockerfile в диркетории на уровне с папками Project/code u Project/tmp. Также необходим плагин с Allure
### 3. Собрать VK MOCK из докер файла, лежащего в директори Project/code
### 4. Запустить Дженкинс командой:
* docker run -d  -v `<YOUR jenkins_home DIR>`:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker-compose):/usr/local/bin/docker-compose  --net host jenkins

### 5. Сбилдить джобу из файла test_qa.yaml в директории Project/tmp/jjb (со своим jenkins.ini разумеется)
#### Примечание: чтобы приложения запускались а после выполлнения тестов отсанавливались у меня был использован плагин PostBuildScript, в джобе test_qa.yaml действия с ним не прописаны, для остановки контейнеров вместо плагина установлен флаг set +e в теле основного шелл скрпта
##Все приготовления совершены

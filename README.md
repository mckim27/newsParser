# newsParser

다음 뉴스 파서. 


# requirements

python 2.7, rabbitmq



# description

다음 뉴스의 텍스트들을 파싱. 처음 시작하는 링크는 http://media.daum.net/economic/ 로 되어 있음.
사회, 정치, 문화 등의 카테고리 홈 주소를 넣을 경우 해당 분야로만 파싱을 수행.
rabbitmq 를 활용하여 병렬 프로그래밍 방식을 흉내.
차후 celery를 활용하여 업그레이드 예정.

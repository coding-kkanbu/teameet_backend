# Change Log

## Unreleased

### Board

- models: Post, Category, Tag, PostLike, Comment, CommentLike, SogaetingOption
- views: PostViewSet, CommentViewSet

### Operation

- models: PostBlame, CommentBlame
- views: PostBlameViewSet, CommentBlameViewSet

### Environment

- set python version 3.8-bullseye

### Github

- set ISSUE_TEMPLATE & PULL_REQUEST_TEMPLATE

### Docs

- README: docker를 이용한 초기 세팅 방법 추가

### Docker

- local.yml: fix docs external port from 7000 to 7777

### CI

- add cache-dependency-path to 'set up python' in linter [cookiecutter-django update](https://github.com/cookiecutter/cookiecutter-django/pull/3520/files)
- change applied branch to 'dev' from 'master'

### THIRD_PARTY_APPS

- dj-rest_auth
  - 사용자 관리를 위한 REST API 패키지 추가
  - 사용자가 소셜 로그인할 수 있도록 구글, 카카오 로그인 rest api로 구현
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)
  - OpenAPI 3.0 문서 생산을 위한 패키지 추가

### Board
- models
  - Post/category field -> ForiegnKey 변경
- serializer:
  - PostSerializer
  - CategorySerializer
  - CommentSerializer
- views
  - PostViewset
  - CategoryViewset
  - CommentViewset

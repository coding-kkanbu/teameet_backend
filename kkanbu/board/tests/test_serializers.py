from django.test import TestCase
from rest_framework.exceptions import ValidationError

from kkanbu.board.models import Post, SogaetingOption
from kkanbu.board.serializers import (
    CommentListSerializer,
    PitAPatSerializer,
    PostSerializer,
    SogaetingOptionSerializer,
)
from kkanbu.users.tests.factories import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    UserFactory,
)


class SogaetingOptionSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory.create(app="PitAPat")
        cls.post = PostFactory.create(category=cls.category)

    def test_validate_wrong_region_fail(self):
        data = {
            "region": "서운",
            "gender": 1,
            "age": 25,
        }
        serializer = SogaetingOptionSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "올바른 지역을 입력해주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["region"]))

    def test_validate_wrong_gender_fail(self):
        data = {
            "region": "서울",
            "gender": 4,
            "age": 25,
        }
        serializer = SogaetingOptionSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "올바른 성별을 입력해주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["gender"]))

    def test_validate_wrong_age_fail(self):
        data = {
            "region": "서울",
            "gender": 2,
            "age": 15,
        }
        serializer = SogaetingOptionSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "올바른 나이를 입력해주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["age"]))

    def test_validate_correct_success(self):
        data = {
            "region": "서울",
            "gender": 1,
            "age": 25,
        }
        serializer = SogaetingOptionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        # serializer fields에 명시되지 않은 field들은 data에 넣어도 처리되지 않음
        serializer.save(post=self.post)
        self.assertTrue(
            SogaetingOption.objects.filter(region="서울", gender=1, age=25).exists()
        )


class PostSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat_topic = CategoryFactory.create(app="Topic", name="Topic 예시")
        cls.cat_pitapat = CategoryFactory.create(app="PitAPat", name="PitAPat 예시")
        cls.user = UserFactory.create()

    def test_validate_wrong_category_fail(self):
        data = {
            "category": self.cat_pitapat.name,
            "title": "테스트 제목",
            "content": "테스트 본문",
            "tags": [],
        }
        serializer = PostSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "게시판에 알맞은 카테고리를 선택해주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["category"]))

    def test_validate_correct_category_success(self):
        data = {
            "category": self.cat_topic.name,
            "title": "테스트 제목",
            "content": "테스트 본문",
            "tags": [],
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save(writer=self.user)
        self.assertTrue(
            Post.objects.filter(
                category=self.cat_topic, title="테스트 제목", content="테스트 본문"
            ).exists()
        )

    def test_validate_title_and_content_length(self):
        data = {
            "category": "Topic 예시",
            "title": "헛",
            "content": "핫",
            "tags": [],
        }
        serializer = PostSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "제목과 내용은 4글자 이상 입력해 주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["title", "content"]))

    def test_timesince_datetime_field_correct(self):
        post = PostFactory.create()
        serializer = PostSerializer()
        self.assertIn("timesince", serializer.to_representation(post))
        self.assertEqual(
            "0\xa0minutes", serializer.to_representation(post)["timesince"]
        )


class PitAPatSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat_topic = CategoryFactory.create(app="Topic", name="Topic 예시")
        cls.cat_pitapat = CategoryFactory.create(app="PitAPat", name="PitAPat 예시")
        cls.user = UserFactory.create()

    def test_validate_wrong_category_fail(self):
        data = {
            "sogaetingoption": {
                "region": "서울",
                "gender": 1,
                "age": 25,
            },
            "category": self.cat_topic.name,
            "title": "테스트 제목",
            "content": "테스트 본문",
            "tags": [],
        }
        serializer = PitAPatSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "게시판에 알맞은 카테고리를 선택해주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["category"]))

    def test_validate_correct_category_success(self):
        data = {
            "sogaetingoption": {
                "region": "서울",
                "gender": 1,
                "age": 25,
            },
            "category": self.cat_pitapat.name,
            "title": "테스트 제목",
            "content": "테스트 본문",
            "tags": [],
        }
        serializer = PitAPatSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save(writer=self.user)
        self.assertTrue(
            SogaetingOption.objects.filter(region="서울", gender=1, age=25).exists()
        )
        self.assertTrue(
            Post.objects.filter(
                category=self.cat_pitapat, title="테스트 제목", content="테스트 본문"
            ).exists()
        )

    def test_validate_title_and_content_length(self):
        data = {
            "sogaetingoption": {
                "region": "서울",
                "gender": 1,
                "age": 25,
            },
            "category": "PitAPat 예시",
            "title": "헛",
            "content": "핫",
            "tags": [],
        }
        serializer = PitAPatSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "제목과 내용은 4글자 이상 입력해 주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["title", "content"]))

    def test_timesince_datetime_field_correct(self):
        post = PostFactory.create()
        serializer = PitAPatSerializer()
        self.assertIn("timesince", serializer.to_representation(post))
        self.assertEqual(
            "0\xa0minutes", serializer.to_representation(post)["timesince"]
        )


class CommentListSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat_topic = CategoryFactory.create(app="Topic", name="Topic 예시")
        cls.post = PostFactory(category=cls.cat_topic)

    def test_validate_comment_length(self):
        data = {
            "post": self.post.id,
            "parent_comment": None,
            "comment": "부족",
        }
        serializer = CommentListSerializer(data=data)
        with self.assertRaisesMessage(ValidationError, "댓글은 4글자 이상 입력해 주세요."):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["comment"]))

    def test_validate_parent_commnet_required(self):
        data = {
            "post": self.post.id,
            "comment": "올바른 길이의 댓글",
        }
        serializer = CommentListSerializer(data=data)
        with self.assertRaisesMessage(
            ValidationError, "이 필드는 필수 항목입니다. 빈 값은 'Null'로 설정해주세요."
        ):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.errors.keys()), set(["parent_comment"]))

    def test_timesince_datetime_field_correct(self):
        comment = CommentFactory.create()
        serializer = CommentListSerializer()
        self.assertIn("timesince", serializer.to_representation(comment))
        self.assertEqual(
            "0\xa0minutes", serializer.to_representation(comment)["timesince"]
        )

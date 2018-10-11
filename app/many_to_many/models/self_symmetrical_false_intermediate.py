from django.db import models
from django.utils import timezone

__all__ = (
    'TwitterUser',
    'Relation',
)


class TwitterUser(models.Model):
    """
    User간의 관계는 2종류로 나뉨
     follow
     block

    관계를 나타내는 Relation클래스 사용 (중개모델)
    """
    name = models.CharField(max_length=50)
    relations = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
    )

    def __str__(self):
        return self.name

    @property
    def followers(self):
        """
        :return: 나를 follow하는 다른 TwitterUser QuerySet
        """
        return TwitterUser.objects.filter(
            from_user_relation__to_use=self,
            from_user_relation__relation_type='f',
        )

    @property
    def following(self):
        """
        :return: 내가 follow하는 다른 TwitterUser QuerySet
        """
        return TwitterUser.objects.filter(
            to_user_relation__from_user=self,
            to_user_relation__relation_type='f',
        )

    @property
    def block_list(self):
        """
        :return: 내가 block하는 다른 TwitterUser QuerySet
        """
        return TwitterUser.objects.filter(
            to_user_relation__from_user='self',
            to_user_relation__relation_type='b',
        )

    def follow(self, user):
        """
        user를 follow하는 Relation을 생성
            1. 이미 존재한다면 만들지 않는다
            2. user가 block_list에 속한다면 만들지 않는다
        :param user: TwitterUser
        :return: Relation instance
        """
        if not self.from_user_relations.filter(to_user=user).exists():
            self.from_user_relations.create(
                to_user=user,
                relation_type='f',
            )
        return self.from_user_relations.get(to_user=user)

    def block(self, user):
        """
        user를 block하는 Relation을 생성
            1. 이미 존재한다면 만들지 않는다
            2. user가 following에 속한다면 해제시키고 만든다
        :param user: TwitterUser
        :return: Relation instance
        """
        try:
            # Relation이 존재함
            relation = self.from_user_relations.get(to_user=user)
            if relation.relation_type == 'f':
                # 근데 following이라면 block으로 바꾸고, 생성일자를 지금 시간으로 변경 후 저장
                relation.relation_type = 'b'
                relation.created_at = timezone.now()
                relation.save()
        except Relation.DoesNotExist:
            # Relation이 없다면 생성 후 생성여부값에 True할당
            relation = self.from_user_relations.create(to_user=user, relation_type='b')
        # Relation인스턴스와 생성여부를 반환
        return relation

    @property
    def follower_relations(self):
        """
        :return: 나를 follow하는 Relation QuerySet
        """
        return self.to_user_relations.filter(relation_type='f')

    @property
    def followee_relations(self):
        """
        :return: 내가 follow하는 Relation QuerySet
        """
        return self.from_user_relations.filter(relation_type='f')


class Relation(models.Model):
    """
    TwitterUser간의 MTM관계를 정의
        from_user
        to_user
        follow인지, block인지를 판단
    """
    CHOICES_RELATION_TYPE = (
        ('f', 'Follow'),
        ('b', 'Block'),
    )
    from_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_user_relation'
    )
    to_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_user_relation'
    )
    # 입력값을 제한하는 choices옵션 추가
    relation_type = models.CharField(
        max_length=1,
        choices=CHOICES_RELATION_TYPE,
    )
    # 관계의 생성일을 기록
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # get_FOO_display() 함수를 사용해서 choices를 사용한 필드의 출력값을 사용
        return 'from({}), to({}), {}'.format(
            self.from_user.name,
            self.to_user.name,
            self.get_relation_type_display(),
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

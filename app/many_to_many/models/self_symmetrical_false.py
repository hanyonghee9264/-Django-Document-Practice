from django.db import models

__all__ = (
    'InstagramUser',
)


class InstagramUser(models.Model):
    name = models.CharField(max_length=50)
    # 내가 folow하고 있는 사람 목록
    # 대칭적이지 않은 다대다 관계
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
    )

    def __str__(self):
        return self.name

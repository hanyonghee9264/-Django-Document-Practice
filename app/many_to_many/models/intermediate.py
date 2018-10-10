from django.db import models

__all__ = (
    'Person',
    'Group',
    'Membership',
)

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

    def __str__(self):
        return self.name


class Membership(models.Model):
    # p1이라는 Person인스턴스가 있을 때
    # Membership.objects.filter(person=p1)
    # Membership.objects.filter(recommender=p1)

    # p1.membership_set.all()
    person = models.ForeignKey(
        Person,
        related_name='memberships',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    recommender = models.ForeignKey(
        Person,
        related_name='memberships_by_recommender',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self):
        return '{person} - {group} ({date})'.format(
            person=self.person.name,
            group=self.group.name,
            date=self.date_joined,
        )

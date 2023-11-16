from rest_framework import serializers
from .models import USER, Coach, Shift, CoachShift, MembershipType, InMemberShip


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = '__all__'


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'



class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class CoachSiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachShift
        fields = '__all__'


class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'


class InMemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = InMemberShip
        fields = '__all__'

    # def set_count_of_remaining_sets(self):
    #     if self.sets_remaining > 0:
    #         self.sets_remaining -= 1
    #         self.checkin_count += 1
    #         self.save()
    #     if self.sets_remaining == 0:
    #         self.delete()
    #     return self.sets_remaining

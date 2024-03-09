from rest_framework import serializers

from api.models import Client, Filter, Mailing, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]
        extra_kwargs = {"name": {"validators": []}}

    def create(self, validated_data):
        return self.Meta.model.objects.get_or_create(**validated_data)[0]


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор клиентов."""

    tag = TagSerializer()

    class Meta:
        model = Client
        fields = ["id", "phone_number", "mobile_operator_code", "tag"]
        read_only_fields = ["id", "mobile_operator_code"]

    def create(self, validated_data):
        received_tag = validated_data.pop("tag")
        tag_object = TagSerializer().create(received_tag)
        return self.Meta.model.objects.create(**validated_data, tag=tag_object)

    def update(self, instance, validated_data):
        received_tag = validated_data.pop("tag")
        tag_object = TagSerializer().create(received_tag)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        instance.tag = tag_object
        instance.save()
        return instance


class FilterSerializer(serializers.ModelSerializer):
    """Сериализатор фильтров."""

    tag = TagSerializer()

    class Meta:
        model = Filter
        fields = ["id", "mobile_operator_code", "tag"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        received_tag = validated_data.pop("tag")
        tag_object = TagSerializer().create(received_tag)
        return self.Meta.model.objects.get_or_create(
            **validated_data, tag=tag_object
        )[0]


class MailingSerializer(serializers.ModelSerializer):
    """Сериализатор рассылок."""

    filter = FilterSerializer()

    class Meta:
        model = Mailing
        fields = [
            "id",
            "start_datetime",
            "end_datetime",
            "message_text",
            "filter",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        received_filter = validated_data.pop("filter")
        filter_object = FilterSerializer().create(received_filter)
        mailing = self.Meta.model.objects.create(
            **validated_data, filter=filter_object
        )
        return mailing

    def update(self, instance, validated_data):
        received_filter = validated_data.pop("filter")
        filter_object = FilterSerializer().create(received_filter)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        instance.filter = filter_object
        instance.save()
        return instance

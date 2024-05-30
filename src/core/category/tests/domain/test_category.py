from uuid import UUID, uuid4

import pytest

from src.core.category.domain.Category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_if_default_id_is_uuid(self):
        category = Category("Test")
        assert isinstance(category.id, UUID)

    def test_if_category_not_accept_name_longer_than_255_chars(self):
        with pytest.raises(ValueError, match="name must not have longer than 255 characters"):
            Category(name="a" * 300)

    def test_category_not_accept_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

    def test_create_category_with_default_values(self):
        category = Category("Teste")
        assert category.description == ""
        assert category.is_active is True

    def test_create_category_with_provided_values(self):
        category_id = uuid4()
        category = Category(name="name", id=category_id, description="Description test", is_active=False)
        assert category.id == category_id
        assert category.description == "Description test"
        assert category.is_active is False


class TestUpdateCategory:
    def test_update_category_name_and_description(self):
        category = Category(name="Name test", description="Description test")

        category.update_category(name="new name", description="new description")

        assert category.name == "new name"
        assert category.description == "new description"

    def test_update_category_with_invalid_name_raise_exception(self):
        category = Category(name="Name test", description="Description test")

        with pytest.raises(ValueError, match="name must not have longer than 255 characters"):
            category.update_category(name="a" * 300, description="")

    def test_update_category_with_empty_name_raise_exception(self):
        category = Category(name="Name test", description="Description test")

        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update_category(name="", description="")


class TestActivateCategory:
    def test_active_inactive_category(self):
        category = Category(name="test", description="", is_active=False)

        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(name="test", description="", is_active=True)

        category.activate()

        assert category.is_active is True


class TestDeactivateCategory:
    def test_deactivate_inactive_category(self):
        category = Category(name="test", description="", is_active=False)

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_active_category(self):
        category = Category(name="test", description="", is_active=True)

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_two_category_have_same_id_they_are_equal(self):
        common_id = uuid4()

        category1 = Category(id=common_id, name="Film")
        category2 = Category(id=common_id, name="Film")

        assert category1 == category2

    def test_equality_different_classes(self):
        common_id = uuid4()

        class Dummy:
            pass

        category = Category(id=common_id, name="Film")
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy

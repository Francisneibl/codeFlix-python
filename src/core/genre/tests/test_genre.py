from uuid import UUID, uuid4

import pytest

from src.core.genre.domain.Genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_cannot_be_empty(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            Genre(name='')

    def test_name_must_have_255_characters(self):
        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            Genre(name='a'*256)

    def test_create_with_default_values(self):
        genre = Genre(name='genre name')
        assert isinstance(genre.id, UUID)
        assert genre.name == 'genre name'
        assert genre.is_active is True
        assert genre.categories == set()

    def test_create_with_provided_values(self):
        genre_id = uuid4()
        category_id = uuid4()
        genre = Genre(
            id=genre_id,
            name='genre name',
            is_active=False,
            categories={category_id}
        )

        assert genre.id == genre_id
        assert genre.name == 'genre name'
        assert genre.is_active is False
        assert genre.categories == {category_id}


class TestChangeName:
    def test_change_genre_name(self):
        genre = Genre(name='Novel')

        genre.change_name(name='Horror')

        assert genre.name == 'Horror'

    def test_cannot_change_to_empty_name(self):
        genre = Genre(name='Novel')

        with pytest.raises(ValueError, match='name cannot be empty'):
            genre.change_name(name='')

    def test_cannot_change_to_name_longer_than_255_characters(self):
        genre = Genre(name='Novel')

        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            genre.change_name(name='a'*256)


class TestActive:
    def test_active_inactive_genre(self):
        genre = Genre(name='Novel', is_active=False)
        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre(name='Novel', is_active=False)
        genre.activate()

        assert genre.is_active is True


class TestDeactivate:
    def test_deactivate_active_genre(self):
        genre = Genre(name='Novel', is_active=True)
        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        genre = Genre(name='Novel', is_active=False)
        genre.deactivate()

        assert genre.is_active is False


class TestAddCategory:
    def test_add_category_in_genre(self):
        category_id = uuid4()
        genre = Genre(name='Novel', is_active=False)
        genre.add_category(category_id)

        assert genre.categories == {category_id}


class TestRemoveCategory:
    def test_remove_category_of_genre(self):
        category_id = uuid4()
        genre = Genre(name='Novel', is_active=False, categories={category_id})
        genre.remove_category(category_id)

        assert genre.categories == set()


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid4()
        genre1 = Genre(id=common_id, name='Genre 1')
        genre2 = Genre(id=common_id, name='Genre 2')

        assert genre1 == genre2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        genre = Genre(id=common_id, name='Genre 1')
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy
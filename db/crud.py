from typing import Any, Dict, List, Optional, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models.models import Group, Image


class ReqouestToDB:
    """
    Класс подготавливает данные для возврата пользователю.
    """

    def __init__(
            self,
            session: AsyncSession,
            groups: Optional[Union[str, List[str]]]
    ) -> None:
        self.session: AsyncSession = session
        self.groups: Optional[Union[str, List[str]]] = groups

    async def change_count_view(
        self,
        model: Image,
        id: int
    ) -> Image:
        """
        Функция для уменьшения счетчика просмотров
        в объекте класса Image.

        Args:
            model (Image): класс Image
            id (int): id объекта в котором
                      изменяется счетчик

        Returns:
            Image: объект класса Image
        """

        obj: Image = await self.session.get(model, int(id))
        obj.count -= 1
        await self.session.commit()
        return obj

    async def select_image_objects(
        self,
        model: Image,
        images: List[str]
    ) -> Dict[str, Union[int, str]]:
        """
        Метод принимает список id изображений в
        базе данных и возвращает данные о нужном для возврата
        пользователю изображении.

        Args:
            model (Image): класс Image
            images (List[str]): список уникальных
                                id изображений

        Returns:
            Dict[str, Union[int, str]]: возвращает словарь
                                        с id изображения и
                                        его url-адресом
        """

        if len(images) > 1:
            max_updated_on = select(
                func.max(model.updated_on)
            ).filter(model.id.in_(images)).as_scalar()
            query = select(model).with_only_columns(
                model.id,
                model.image_url
            ).filter(
                model.id.in_(images),
                model.updated_on < max_updated_on,
                model.count == select(
                    func.max(model.count)
                ).filter(
                    model.id.in_(images)
                ).filter(model.updated_on < max_updated_on).as_scalar()
            )
        else:
            query = select(model).with_only_columns(
                model.id,
                model.image_url
            ).filter(model.id == int(images[0]))
        image_objs = await self.session.execute(query)
        image_data = image_objs.fetchone()
        await self.change_count_view(model, image_data.id)
        return {'id': image_data.id, 'image_url': image_data.image_url}

    async def select_group_objects(
        self,
        model: Group,
        groups: Optional[Union[str, List[str]]]
    ) -> Union[List[Any], Dict[str, Union[int, str]]]:
        """
        Метод получает данные о запрашиваеых пользователем группах
        и возвращает список id изображений для этих групп либо пустой
        список если ничего не найдено.

        Args:
            model (Group): класс Group
            groups (Optional[Union[str, List[str]]]): названия запрашиваемых
                                                      групп

        Returns:
            Union[List[Any], Dict[str, Union[int, str]]]: Список id изображений
                                                          или пустой список
                                                          если нет доступных
                                                          для просмотра
                                                          изображений
        """

        if groups:
            query = select(model).filter(model.title.in_(groups))
        else:
            query = select(model)
        query = query.options(selectinload(model.images))
        group = await self.session.execute(query)
        if group is not None:
            images = list({
                image.id
                for group in group.scalars()
                for image in group.images
                if image.count > 0
            })
            if images:
                return await self.select_image_objects(Image, images)
        return []

    async def get_data(self) -> Union[List[Any], Dict[str, Union[int, str]]]:
        """
        Метод возвращает данные изображения для возврата пользователю.

        Returns:
            _type_: _description_
        """
        return await self.select_group_objects(
            Group,
            self.groups
        )

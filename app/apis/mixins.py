from rest_framework import viewsets

import logging

logger = logging.getLogger("api")


class CRUDModelViewSetMixin(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        logger.info("{} on {} by {}".format(self.action.upper(),
                                            self.__class__.__name__,
                                            self.request.user))
        return super(CRUDModelViewSetMixin, self).perform_create(serializer)

    def perform_update(self, serializer):
        logger.info("{} on {} by {}".format(self.action.upper(),
                                            self.__class__.__name__,
                                            self.request.user))
        return super(CRUDModelViewSetMixin, self).perform_update(serializer)

    def perform_destroy(self, instance):
        logger.info("{} on {} by {}".format(self.action.upper(),
                                            self.__class__.__name__,
                                            self.request.user))
        return super(CRUDModelViewSetMixin, self).perform_destroy(instance)

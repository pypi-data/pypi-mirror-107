from bergen.messages.postman.log import LogLevel
from bergen.messages.postman.provide.provide_log import ProvideLogMessage
from bergen.messages.postman.provide.provide_critical import ProvideCriticalMessage
from bergen.messages.postman.provide.provide_done import ProvideDoneMessage
from typing import Dict
from bergen.schema import Template
from bergen.messages.postman.assign.assign_done import AssignDoneMessage
from bergen.debugging import DebugLevel
from bergen.handlers.base import ContractHandler
from bergen.messages import BouncedProvideMessage
from bergen.console import console


class ProvideHandler(ContractHandler[BouncedProvideMessage]):

    @property
    def template_id(self) -> str:
        return self.message.data.template

    @property
    def bounced(self):
        return self.message.meta.token

    @property
    def meta(self):
        return {"extensions": self.message.meta.extensions, "reference": self.message.meta.reference}

    @property
    def template_id(self) -> str:
        return self.message.data.template

    @property
    def context(self) -> Dict:
        if self.context_set is False:
            console.log("Context was never set, no sense in accessing it...")
            return {}
        return self.active_context

    async def log(self, message, level =LogLevel.INFO):
        console.log(message)
        await self.pass_log(str(message), level=level)   

    def set_context(self, context):
        self.context_set = True
        self.active_context = context

    async def pass_done(self):
        provide_done = ProvideDoneMessage(data={"ok": True}, meta=self.meta)
        return await self.forward(provide_done)

    async def pass_log(self, message: str, level = LogLevel.INFO):
        provide_log = ProvideLogMessage(data={"message": message, "level": level.value}, meta=self.meta)
        return await self.forward(provide_log)

    async def get_template(self) -> Template:
        return await Template.asyncs.get(id=self.message.data.template)

    async def pass_exception(self, exception):
        critical_message = ProvideCriticalMessage(data={"message": str(exception), "type": exception.__class__.__name__}, meta=self.meta)
        return await self.forward(critical_message)
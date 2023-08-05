# drf-ebs-utils

**drf-ebs-utils** is a package that offers service classes for notification-service , attachment-service , sso-service.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install drf_ebs_utils.

```bash
pip install drf_ebs_utils
```

Setting `.env`
```shell
SERVICE_SSO_DOMAIN=
SERVICE_SSO_SERVICE_TOKEN=
SERVICE_SSO_SECRET_TOKEN=
SERVICE_SSO_SECRET_KEY=

SERVICE_NOTIFICATION_HOST=
SERVICE_NOTIFICATION_SECRET_KEY=

SERVICE_ATTACHMENT_HOST=
SERVICE_ATTACHMENT_SECRET_KEY=
SERVICE_ATTACHMENT_SECRET_TOKEN=
```

## Available service classes

* SSOService
* NotificationService
* AttachmentService

## Usage

Example
```
from drf_ebs_utils.services.sso import SSOService
sso = SSOService()

from drf_ebs_utils.services.notification import NotificationService
notification = NotificationService()

from drf_ebs_utils.services.attachment import AttachmentService
attachment = AttachmentService()
```

## Contributing

Pull requests are welcome. Open issues addressing pull requests.

## License

[MIT](https://choosealicense.com/licenses/mit/)
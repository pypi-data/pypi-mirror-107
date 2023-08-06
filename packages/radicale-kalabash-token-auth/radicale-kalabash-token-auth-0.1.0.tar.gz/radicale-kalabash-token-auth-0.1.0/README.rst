radicale-kalabash-token-auth
===========================

A token based authentication plugin for Radicale provided by
Kalabash. If the authentication fails, it will fallback to dovecot
authentication plugin.

Installation
------------

You can install this package from PyPi using the following command::

   pip install radicale-kalabash-token-auth

Configuration
-------------

Here is a configuration example::

   [auth]
   type = radicale_kalabash_token_auth

   radicale_kalabash_token_auth_check_url = https://my.kalabash.com/api/v1/user-calendars/check_token/
   radicale_kalabash_token_auth_token = MYTOKENHERE

The `token` setting corresponds to a valid Kalabash API token.

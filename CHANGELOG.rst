Changelog
=========

2.3.0 (2025-05-12)
------------------

- Add custom exception-handler to handle JobTimeoutException when task exceeded maximum timeout value.
  [cekk]
- Send to endpoint also an error_message.
  [cekk]
- Handle smtp timeout (default 120s) and made it configurable.
  [cekk]

2.2.2 (2025-03-21)
------------------

- Increase job_timeout to 30s to better handle retries.
  [cekk]

2.2.1 (2025-01-16)
------------------

- Improve Exceptions handling in background_task. Now it will retry the task three times if it fails.
  [cekk]
- Fix bug in send_complete method and return proper status when there is an error.
  [cekk]

2.1.0 (2024-03-14)
------------------

- Open a new smtp connection for each recipient (because new RER smtp server has a 10min timeout).
  [cekk]

2.0.1 (2023-02-15)
------------------

- Fix dependencies versions.
  [cekk]


2.0.0 (2021-11-04)
------------------

- Use flask-mailman instead of unmaintained flask-mail.
  [cekk]


1.1.0 (2021-05-21)
------------------

- Handle Exceptions and return error state.
  [cekk]
- Handle attachments.

1.0.1 (2020-09-08)
------------------

- Dynamic job_timeout based on number of recipients.
  [cekk]
- Log progress status each 1000 sent mails.
  [cekk]

1.0.0 (2020-07-27)
------------------

- Initial release.
  [cekk]

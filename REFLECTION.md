# Engineering Reflection

## 1. What assumptions did you make?

I treated the legacy portal as a read-only system and used its existing
authenticated endpoints instead of modifying the portal. I assumed the
observed response fields and endpoint paths would remain stable during
normal use. I chose snake_case field names and numeric types for measurements
to make the wrapper easier for API consumers to use.

## 2. Which part was the most difficult, and how did you get unstuck?

The most difficult part was understanding how the portal worked behind its
web interface, especially authentication and session cookies. I used the
browser's Network panel to inspect requests and responses, then reproduced
the observed login behavior with HTTPX. Testing each endpoint independently
helped me identify and resolve issues.

## 3. If you had another day, what would you improve?

I would add broader automated tests using mocked portal responses, verify
session expiry and retry behavior, improve error mapping, and handle malformed
or unexpected legacy responses. I would also investigate the portal's meter
detail page and network hierarchy to expose richer meter information.

## 4. What mistake did you make while solving this?

My initial Python login request returned HTTP 403 because it did not reproduce
the request behavior expected by the portal. Inspecting the successful browser
request helped me identify the additional headers needed. This reinforced
the importance of observing the actual protocol instead of guessing.

## 5. If you were reviewing your own submission, what would you criticise?

The implementation is intentionally small, but it needs stronger automated
coverage for failures and authentication edge cases. The meter detail
endpoint currently finds an exact ID through search results rather than
parsing the dedicated detail page. I would also review pagination metadata,
resource cleanup, and the handling of upstream timeouts and errors before
using the service in production.

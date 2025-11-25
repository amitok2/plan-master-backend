# 🔒 Security Guidelines

## API Key Management

### Backend Configuration

The Plan Master Backend **requires** API keys to be set via the `PLAN_MASTER_API_KEYS` environment variable.

**There is NO default API key** - this is intentional for security.

### Setting Up API Keys

#### For Local Development:

1. Create a `.env` file in the backend directory:
   ```bash
   # .env (NEVER commit this file!)
   GEMINI_API_KEY=your-gemini-api-key
   PLAN_MASTER_API_KEYS=pm_dev_local_key_12345
   ```

2. The `.env` file is already in `.gitignore` - keep it there!

#### For Production (Render):

1. Go to your Render dashboard
2. Navigate to **Environment** tab
3. Add environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `PLAN_MASTER_API_KEYS`: Comma-separated list of secure keys

### Generating Secure API Keys

**NEVER use simple keys like `test-key-123` in production!**

Generate secure keys using:

```bash
# Python method (recommended)
python3 -c "import secrets; print('pm_' + secrets.token_urlsafe(32))"

# OpenSSL method
openssl rand -base64 32 | tr -d "=+/" | cut -c1-32

# Node.js method
node -e "console.log('pm_' + require('crypto').randomBytes(32).toString('base64url'))"
```

Example output:
```
pm_7k9mX2nQ8pL4vR6wY3jT5hB1cN0zF9dH8sK4mP2qW6yL
```

### Key Rotation

For security, rotate your API keys regularly:

1. Generate a new key
2. Add it to `PLAN_MASTER_API_KEYS` (comma-separated with old key)
3. Update clients to use the new key
4. After all clients are updated, remove the old key

Example during rotation:
```bash
PLAN_MASTER_API_KEYS=old-key-still-valid,new-key-preferred
```

### Multiple Keys

You can issue different keys for different purposes:

```bash
# Example: Different keys for different clients or environments
PLAN_MASTER_API_KEYS=pm_client_a_key,pm_client_b_key,pm_internal_key
```

## What NOT to Do

❌ **DON'T** hardcode API keys in code  
❌ **DON'T** commit `.env` files to Git  
❌ **DON'T** share API keys in public documentation  
❌ **DON'T** use simple/guessable keys like `test-key-123`  
❌ **DON'T** reuse keys across different projects  

## What TO Do

✅ **DO** use environment variables for all secrets  
✅ **DO** generate cryptographically secure random keys  
✅ **DO** rotate keys regularly  
✅ **DO** use different keys for dev/staging/production  
✅ **DO** keep `.env` in `.gitignore`  
✅ **DO** document key requirements without exposing actual keys  

## Backend Behavior

### Without API Keys Set

If `PLAN_MASTER_API_KEYS` is not set, the backend will:
- ✅ Start successfully
- ⚠️ Log a critical warning
- ❌ Reject all API requests with `401 Unauthorized`

This is intentional - it's better to fail closed than to have a default key.

### With API Keys Set

The backend will:
- ✅ Accept requests with valid `Authorization: Bearer <key>` header
- ❌ Reject requests without the header
- ❌ Reject requests with invalid keys

## Checking Your Setup

### Test if API keys are working:

```bash
# Should return 401 Unauthorized (no key)
curl https://plan-master-backend.onrender.com/health

# Should return 200 OK (with valid key)
curl https://plan-master-backend.onrender.com/health \
  -H "Authorization: Bearer your-valid-key-here"
```

### Check backend logs:

If you see this warning in logs:
```
CRITICAL: PLAN_MASTER_API_KEYS environment variable is not set!
```

Then you need to set the environment variable in Render.

## For MCP Client Users

Users of the MCP client need to:
1. Get an API key from you (the backend operator)
2. Set it in their MCP configuration:
   ```json
   {
     "mcpServers": {
       "plan-master": {
         "command": "npx",
         "args": ["-y", "plan-master-mcp"],
         "env": {
           "PLAN_MASTER_API_KEY": "their-issued-key-here"
         }
       }
     }
   }
   ```

## Issuing Keys to Users

When issuing keys to MCP users:

1. Generate a unique key for each user/organization
2. Keep a record of which key belongs to whom
3. Consider adding key prefixes for identification:
   - `pm_user_<name>_<random>`
   - `pm_org_<org>_<random>`
4. Set expiration dates if needed
5. Have a process for revoking compromised keys

## Incident Response

If a key is compromised:

1. **Immediately** remove it from `PLAN_MASTER_API_KEYS`
2. Redeploy the backend (Render will pick up the change)
3. Generate a new key for the affected user
4. Notify the user of the compromise
5. Review logs for unauthorized usage

## Questions?

If you have security concerns or questions:
- Open an issue on GitHub (without exposing keys!)
- Contact the maintainers privately
- Review the code - it's open source!

---

**Remember:** Security is not a feature, it's a requirement. Treat API keys like passwords - never expose them publicly.


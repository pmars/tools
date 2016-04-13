local redis = require "resty.redis"
local cjson = require "cjson"
local fun = require "fun"
local cache = redis:new()
local ok, err = cache:connect("127.0.0.1", "6379")
local header = ngx.req.get_headers()
local user = header["X-USERNAME"]
local token = header["X-AUTH-TOKEN"]
local uri = ngx.var.uri
ngx.req.read_body()
local body = ngx.req.get_body_data()
local request_method = ngx.var.request_method

if body == ngx.null or body == nil then
    ngx.say(header['Content-Length'])
    ngx.say('body is nil')
    ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
end

if not ok then
    ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
end

if request_method == "GET" then
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

cache:set_timeout(60000)
local res, err = cache:get(user)

if res == ngx.null or res == nil then
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

if res ~= token then
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

db_table_name = uri
db_table_name = db_table_name:gsub("/[vV]1/", "")
db_table_name = db_table_name:gsub("/$", "")
db_table_name = db_table_name:gsub("/", "_")

local port, err = cache:get(db_table_name)
if port == ngx.null or port == nil then
    ngx.say("table:\'"..uri.."\' not set any port now.")
end

function cvt(x)
    return {body=cjson.encode(x)}
end

body_json = cjson.decode(body)
body_fun = fun.map(cvt, body_json)
body_str = cjson.encode(fun.totable(body_fun))

local proxy_url = "/proxy/"..port
local res = ngx.location.capture(proxy_url, {
        method = ngx.HTTP_POST,
        body = body_str
    })

ngx.say(res.status)
ngx.say(res.body)

if res.status ~= ngx.HTTP_OK then
    ngx.say("service run failed, proxy pass failed")
    return
end

local pool_max_idle_time = 10000
local pool_size = 100
local ok, err = cache:set_keepalive(pool_max_idle_time, pool_size)

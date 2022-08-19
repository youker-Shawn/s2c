import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import MyUser


# Create your views here.
@csrf_exempt
def register(request):
    """用户注册"""
    if request.method == 'POST':
        post_data = json.loads(request.body)
        name = post_data.get('username', '')
        invite_code = post_data.get('invite', '')
        if not name:
            return JsonResponse(api_response(400, "必传参数缺失"))

        try:
            # 注册的同时uuid生成个人的邀请码。邀请人可选
            inviter = MyUser.objects.filter(invite=invite_code)
            if inviter:
                MyUser.objects.create(username=name, invitedby=inviter.first().pk)
            else:
                MyUser.objects.create(username=name)
        except Exception as e:
            print(e)
            return JsonResponse(api_response(500, "注册失败"))

        return JsonResponse(api_response(201, "注册成功"))


def api_response(code=200, msg="", result=None, status="success"):
    """统一的后端接口返回内容格式
    """
    # 默认值
    ret = {
        "code": code,
        "status": status,
        "message": msg,
        "result": result if result else {},
    }

    if str(code).startswith("2") or str(code).startswith("3"):  # 2XX 3XX
        ret["status"] = "success"
    elif str(code).startswith("4"):  # 4XX
        ret["status"] = "error"
    elif str(code).startswith("5"):  # 5XX
        ret["status"] = "fail"
    else:
        pass  # 其他自定义code，默认为success

    # return JsonResponse(ret)  # Django传统的Json返回方式
    return ret  # 便于DRF直接使用的Json返回方式

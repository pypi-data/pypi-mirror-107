# coding: utf8
from jinja2.sandbox import SandboxedEnvironment
from farbox_bucket.utils.convert.jade2jinja import convert_jade_to_html

def get_jinja_source_code_from_jade(jade_content, with_lines=True):
    source_code_lines = []
    html_content = convert_jade_to_html(jade_content)
    env = SandboxedEnvironment()
    #env.compile(html_content)
    source = env._parse(html_content, None, None)
    python_code = env._generate(source, None, None, False)
    python_lines = python_code.split("\n")
    for (i, python_line) in enumerate(python_lines):
        if with_lines:
            source_code_lines.append("%s:%s" % (i+1, python_line))
        else:
            source_code_lines.append(python_line)
    return "\n".join(source_code_lines)


def print_jinja_source_code_from_jade_file(jade_filepath):
    with open(jade_filepath) as f:
        jade_content = f.read()
    source_code = get_jinja_source_code_from_jade(jade_content, with_lines=True)
    print(source_code)


raw_content = """html
	head
		title Merge to FarBox 2.0 Balance
	body
		+account.need_login()

		+site.system_nav(30)

		h1(style="text-align:center;width:550px;margin:0 auto;padding-top:45px;padding-bottom:30px;")= "转移账户余额为 FarBox 2.0 有效期天数"

		if request.method == 'POST'
			.account_info(style="width:550px;margin:0 auto;padding-top:30px;")
				h2 Result
				if info
					span Information:
					span= info

		keys = ["farbox_bucket`Bucket or Domain`", "bucket_type@select`￥128, ￥299`", "action@select`显示转换信息, 确定并转移余额`"]
		+h.simple_form(keys=keys, data_obj={'farbox_bucket':request.values.farbox_bucket or ''}, submit_text="提交")

		div.note(style="width:550px;margin:0 auto;padding-bottom:50px;font-size:13px;color:#333")
			p 说明：
			p 此处仅仅处理账户内余额迁移到 FarBox 2.0 的某个 Bucket 中，不做其它数据的迁移；
			p 仅允许迁移一次，之后，Bitcron 上的余额会扣减会负，并且后续 Bitcron 上不能再进行充值！
			p 先『显示转换信息』后，再进行『确定并转移余额』的操作。
"""
print(get_jinja_source_code_from_jade(raw_content, with_lines=True))
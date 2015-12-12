
set nocompatible
set autoindent			"自动缩进
set cindent				
set showmatch			"代码匹配
set softtabstop=4		
set shiftwidth=4		
set tabstop=4
set noet				
set nu					
set hlsearch			"检索时高亮显示匹配项
set ruler				
set ru					
set colorcolumn=90		
set ignorecase			
set helplang=cn			"帮助系统设置为中文
set showcmd				"输入的命令显示出来，看的清楚些
set foldenable			"允许折叠
set foldmethod=syntax	"手动折叠
set backspace=indent,eol,start			
set completeopt=preview,longest,menu
set ruler				"打开状态栏标尺
"" set cursorline			"突出显示当前行
set expandtab

set list listchars=tab:→\ ,trail:·

colorscheme desert

if &term=="xterm"
	set t_Co=8
	set t_Sb=^[[4%dm
	set t_Sf=^[[3%dm
endif

""新建 .sh, .py 文件，自动插入文件头
autocmd BufNewFile *.py,*.sh exec ":call SetTitle()"
""定义函数SetTitle，自动插入文件头
func SetTitle()
	if &filetype == 'sh'
		call setline(1, "\#!/bin/bash")
		call append(line(".")+0, "")
		call append(line(".")+1, "\#############################################")
		call append(line(".")+2, "\# File Name: ".expand("%"))
		call append(line(".")+3, "\# Author: xingming")
		call append(line(".")+4, "\# mail: huoxm@zetyun.com")
		call append(line(".")+5, "\# Created Time: ".strftime(" %Y-%m-%d %X"))
		call append(line(".")+6, "\#############################################")
		call append(line(".")+7, "")
		call append(line(".")+8, "")
	else 
		call setline(1, "\#!/usr/bin/env python")
		call append(line(".")+0, "\#-*- coding:utf-8 -*-")
		call append(line(".")+1, "")
		call append(line(".")+2, "\#############################################")
		call append(line(".")+3, "\# File Name: ".expand("%"))
		call append(line(".")+4, "\# Author: xingming")
		call append(line(".")+5, "\# Mail: huoxm@zetyun.com ")
		call append(line(".")+6, "\# Created Time: ".strftime(" %Y-%m-%d %X"))
		call append(line(".")+7, "\#############################################")
		call append(line(".")+8, "")
		call append(line(".")+9, "")
		call append(line(".")+10, "")
		call append(line(".")+11, "")
		call append(line(".")+12, "def main():")
		call append(line(".")+13, "    print 'hello'")
		call append(line(".")+14, "")
		call append(line(".")+15, "if __name__ == \"__main__\":")
		call append(line(".")+16, "    main()")
		call append(line(".")+17, "")
	endif

	autocmd BufNewFile * normal G
endfunc


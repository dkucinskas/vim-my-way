set cc=80
set ruler

set listchars=tab:>-,trail:-
set list

let s:showMakeWnd = "0"
let b:comment_leader = '// '

function! Lint()
    setlocal makeprg=jslint\ %
    setlocal errorformat=%f:%l:%c:%m

	echo "Make Wnd mode: " . s:showMakeWnd
	
	if s:showMakeWnd == "0"
		w
		silent make
		cw
		copen
		cc
	else
		cclose
	endif
	
	let s:showMakeWnd = (s:showMakeWnd == "0" ? "1" : "0")
endfunction

function! Run()
    setlocal makeprg=node\ %
    setlocal errorformat=%f:%l:%c:%m

	echo "Make Wnd mode: " . s:showMakeWnd
	
	if s:showMakeWnd == "0"
		w
		silent make
		cw
		copen
		cc
	else
		cclose
	endif
	
	let s:showMakeWnd = (s:showMakeWnd == "0" ? "1" : "0")
endfunction

"function! CommentToggle()
""    execute ':silent! s/\([^ ]\)/\/\/ \1/'
""    execute ':silent! s/^\( *\)\/\/ \/\/ /\1/'
"    execute ':silent! s,^\(\s*\)[^# \t]\@=,\1# ,e<CR>:nohls<CR>zvj'
"    execute ':silent! s,^\(\s*\)# \s\@!,\1,e<CR>:nohls<CR>zvj'
"endfunction

nmap <silent> <F5> :call Lint()<CR>
nmap <silent> <F6> :call Run()<CR>
nmap <silent> <F7> :!node-debug %<CR>

" toggle comments
noremap <silent> ,cc :<C-B>silent <C-E>s/^/<C-R>=escape(b:comment_leader,'\/')<CR>/<CR>:nohlsearch<CR>
noremap <silent> ,cu :<C-B>silent <C-E>s/^\V<C-R>=escape(b:comment_leader,'\/')<CR>//e<CR>:nohlsearch<CR>
"noremap <silent> ,cc :call CommentToggle()<CR>


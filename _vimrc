set nocompatible

call pathogen#infect()
call pathogen#helptags()

syntax on
filetype plugin indent on

set clipboard=unnamed								" paste from system cilpbord
set encoding=utf-8									" set encoding to UTF-8
set showcmd											" show incoplete commands

"" Swap and backup files
set nobackup
set nowritebackup
set noswapfile

"" Code
syntax enable										" synatx highlighting always on
filetype plugin indent on							" turn automatic filetype detection on
set number											" show line numbers

if version >= 730									" vertical guidline 80 column
	if has('gui_running')							" works only since 7.3 version
		set colorcolumn=80
	endif
endif

"" Tab width and whitespace
set nowrap
set showtabline=4
set softtabstop=4
set tabstop=4
set shiftwidth=4
set expandtab " replaces tabs with spaces 
set backspace=indent,eol,start						" backspace throuht everything in insert mode

"" Spelling
set spell

"" Colorscheme
set background=dark
"set background=light
"colo codeschool
"colo github
"colo hemisu
colo molokai
"colo solarized

"if has('autocmd')
"	autocmd WinEnter,FileType sh,c,h colorscheme vividchalk
"	autocmd WinEnter,FileType * colorscheme solarized
"endif

" Set GUI options
if has('gui_running')
	set guioptions-=m								" remove menu bar
	set guioptions-=T								" remove toolbar
	set guioptions-=r								" remove right-hand scroll bar
	
	if has('gui_win32')
		"set guifont=Consolas:h10:cANSI
		set Envy\ Code\ R:h11:cANSI
	elseif has('gui_gtk')
		"set guifont=Inconsolata\ 12
		"set guifont=Droid\ Sans\ Mono\ 12
		set guifont=DejaVu\ Sans\ Mono\ 12
	endif
	
	autocmd vimenter * NERDTree
    autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif
endif

vmap <Tab> >gv
vmap <S-Tab> <gv

" Map tabnext, tabprevious and tabnew (like firefox)
map <C-tab> :tabnext<CR>
map <C-S-tab> :tabprevious<CR>
nmap <C-t> :tabnew<CR>i
imap <C-t> <ESC>:tabnew<CR>i


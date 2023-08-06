au VimEnter * :3 windo resize 1
au VimEnter * :1 wincmd W

set complete=k
set completeopt=preview

set shortmess=a
set shortmess+=F

inoremap <Tab> <C-n>

nnoremap <Tab> <C-w>w
inoremap <S-Tab> <Tab>

nnoremap <Up> :wincmd W<CR>
inoremap <Up> <Esc>:wincmd W<CR>i
nnoremap <Down> :wincmd w<CR>
inoremap <Down> <Esc>:wincmd w<CR>i

nnoremap <CR> :xa<CR>

set stl=%t
set noruler

set noshowcmd
set shortmess+=F

hi StatusLine cterm=bold
hi StatusLine ctermbg=16
hi StatusLine ctermfg=1
hi StatusLineNC cterm=bold
hi StatusLineNC ctermbg=16
hi StatusLineNC ctermfg=2


set fillchars=eob:\ ,

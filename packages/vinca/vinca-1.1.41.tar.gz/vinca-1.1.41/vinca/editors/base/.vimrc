au VimEnter * :3 windo resize 1
au VimEnter * :1 wincmd W

set complete=k
set completeopt=preview


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

<header class="article-header">
    <h1>My Dotfile Setup</h1> Published <time datetime="2023-09-18">2023-09-18</time> by James Frost.
    <p class="tagline">How I manage my configuration.</p>
</header>

***TODO: Rewrite this into a proper article. It is currently a mess of notes to self.***

---

My dotfile setup is a slightly adapted variant of the one described at [atlassian.com/git/tutorials/dotfiles](https://www.atlassian.com/git/tutorials/dotfiles).

This means that the only hard dependency is git (though curl and sh are nice to have for the restore script). It also doesn't cause confusion by making my entire home directory appear to be a git repository, which [Drew DeVault's method does](https://drewdevault.com/2019/12/30/dotfiles.html)).

For completeness (and preventing death by 404) I'll rewrite the method here. The key changes I've made are as follows:

* Renamed the alias to `dotfile`. Given that is the obvious name to me.
* Added a wildcard .gitignore, so you can `dotfile add .` changes. Hence need to use --force when adding things for the first time. Hidden as .dotfiles/info/exclude
* Adding a nice interactive script when restoring the dotfiles.

The key to this method is using a bare repository with a custom alias of git that sets the working dir to `$HOME`.

## First time setup

This is for creating the repository the first time, and should only be necessary once.

```sh
git init --bare $HOME/.dotfiles
alias dotfile='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
echo "alias dotfile='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'" >> $HOME/.bashrc
printf '\n*\n' >> $HOME/.dotfiles/info/exclude
dotfile config --local status.showUntrackedFiles no
```

Then push to a remote like GitHub.

## Adding configs
Adding configurations is quite simple. The only difference from normal git usage is the force add.

`dotfile add --force example.conf` to add a config for the first time.

`dotfile status` to see which configs have uncommitted changes.

`dotfile add .` to add all uncommitted changes.

Then `git push` to your remote.

## Restoring to a new system

There is a script to do this with an interactive installer. This can be run directly with:

***TODO: Setup redirect from a shorter URL.***

```sh
curl -LsSf https://gist.githubusercontent.com/Fraetor/059207afa6a1791f480586cf52b19a76/raw/ >install-dotfiles.sh && sh install-dotfiles.sh
```

[The below script](https://gist.github.com/Fraetor/059207afa6a1791f480586cf52b19a76) checks out the repository and sets everything up. The only prerequisites are that sh and git are installed, and that SSH authentication is setup with the repository remote.

<script src="https://gist.github.com/Fraetor/059207afa6a1791f480586cf52b19a76.js"></script>

## Machine specific configs

These can be stored on separate branches. As the main idea with dotfiles is to have a unified config everywhere there shouldn't be a huge amount of difference from the main branch, but it can still be useful to have some. Branches should be regularly rebased on main, perhaps by CI?

## Known issues

### ~/.gitconfig cannot be managed across identities

A gitconfig file contains many useful aliases and tweaks for git. Unfortunately this dotfile manager cannot handle this file, at least not across systems.
Another thing contained within a gitconfig file is the committer identity and a reference to the signing key git uses. This will always be per system, as the private signing keys should not leave the system they were generated on.

Unfortunately the standard method of having per system branches does not work as many operations checkout these branches and fail when they can't find the correct signing keys due to the gitconfig being reread mid-rebase.

Perhaps it would be possible to make a special copy for dotfile to use during a rebase, but its really not worth it.

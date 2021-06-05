<div align="center">
	<h1>rfcdl</h1>
	<h4 align="center">
		Always keep a copy of your favorite <a href="https://www.ietf.org/standards/rfcs/">RFCs</a>.
	</h4>
	<p>rfcdl lets you download and synchronize RCFs in high-speed.</p>
</div>

<p align="center">
	<a href="https://github.com/eikendev/rfcdl/actions"><img alt="Build status" src="https://img.shields.io/github/workflow/status/eikendev/rfcdl/Main"/></a>&nbsp;
	<a href="https://pypi.org/project/rfcdl/"><img alt="Development status" src="https://img.shields.io/pypi/status/rfcdl"/></a>&nbsp;
	<a href="https://github.com/eikendev/rfcdl/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/rfcdl"/></a>&nbsp;
	<a href="https://pypi.org/project/rfcdl/"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/rfcdl"/></a>&nbsp;
	<a href="https://pypi.org/project/rfcdl/"><img alt="Version" src="https://img.shields.io/pypi/v/rfcdl"/></a>&nbsp;
	<a href="https://pypi.org/project/rfcdl/"><img alt="Downloads" src="https://img.shields.io/pypi/dm/rfcdl"/></a>&nbsp;
</p>

## 🚀&nbsp;Installation

### From PyPI

```bash
pip install rfcdl
```

### From Source

```bash
./setup.py install
```

### Fedora

```bash
sudo dnf copr enable eikendev/rfcdl
sudo dnf install python3-rfcdl
```

## 📄&nbsp;Usage

This tool can be used to download a large number of [RFC documents](https://www.ietf.org/standards/rfcs/) in a short period of time.
I used it to keep a local mirror of all RFCs on my machines continuously synchronized.

For a quick introduction, let me show how you would use the tool to get started.

This is how you download the RFCs initially.

```bash
rfcdl -d ~/download/rfc/
```

As can be seen above, you have to specify a directory where all RFC documents will be saved in.
Upon the next invocation of `rfcdl`, only the RFCs missing in that directory will be downloaded.

This can then be combined with an alias that lets you read the local copy of any RFC.
The following command opens the RFC 8032 for me in less.

```bash
rfc 8032
```

Check out [my dotfiles](https://github.com/eikendev/dotfiles/blob/199faa40873d8757a7c8f63d82d0f18a83b74ef9/source/zsh/function/rfc.zsh) to see how this is implemented.

### Arguments

If you only want to download a random subset of all RFCs, use the `--samples` flag.
This can be used for testing.
For instance, the following will download 20 random RFC documents.

```bash
rfcdl -d ~/download/rfc/ --samples 20
```

Since `rfcdl` downloads multiple files in parallel by default, one can specify how many simultaneous downloads are allowed using the `--limit` flag.
The following invocation will only download at most ten files in parallel.

```bash
rfcdl -d ~/download/rfc/ --limit 10
```

To explicitly state how many times `rfcdl` should download a file upon error, the `--retries` flag can be used.
This can be useful in case one expects a bad connection.
This is how you could tell the tool to try to download each file at maximum five times.

```bash
rfcdl -d ~/download/rfc/ --retries 5
```

## ⚙&nbsp;Configuration

A configuration file can be saved to `~/.config/rfcdl/config.ini` to avoid specifying the path for each invocation.
Of course, `$XDG_CONFIG_HOME` can be set to change your configuration path.
Alternatively, the path to the configuration file can be set via the `--config-file` argument.

```ini
[GENERAL]
RootDir = ~/download/rfc/
```

## 💻&nbsp;Development

The source code is located on [GitHub](https://github.com/eikendev/rfcdl).
To check out the repository, the following command can be used.

```bash
git clone https://github.com/eikendev/rfcdl.git
```

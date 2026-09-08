## The Tools Are Not the Work

### Chapter Nine

The rest of this book would be the same book in 1995. This chapter would
not. Everything in it is about a set of tools that arrived very fast, and it
is written down partly because it is useful now and partly because it will
be a record of what this period actually felt like from inside it.

### On choosing a language

At the start of your career, choosing the *best* programming language and
debating what is best is not worth it. Doing that is how you spend time not
learning to code. Changing later is not hard, as long as you pick something
in the top fifteen and not Assembly. Pick one based on what you want to
build, and go.

Learn the beginner material once, then learn by building projects. Project
based learning wins. Courses are fine if they work for you.

### On models and workflow

One thing I realised after using AI tools heavily is that **the workflow
matters more than the model**. People argue about which model is best. In
practice, productivity comes from using the right tools together, not from
picking a winner. Benchmarks are not accurate but they give a rough sense of
what is strong right now. Do not obsess over leaderboards.

Sometimes the best way to save tokens is to spend more of them, in the right
places. Force one expensive model to do everything and you burn an absurd
amount for no gain. Split the work: large mechanical tasks, big refactors,
repetitive edits, formatting, all of it goes to whatever tool charges per
request instead of per token. Reasoning and complex change goes to the
strongest model you have. Using each tool for what it is good at saves both
time and money.

And write the prompt properly. If you do not understand what you wrote, the
model is not going to either.

### On agents, honestly

There is a lot of hype about agents building software by themselves. It is
not there yet, and the failure modes are specific.

- **Context.** Most agents cannot see the whole codebase at once, so they
  break things without noticing.
- **Error loops.** The agent makes a mistake, then keeps fixing its own
  mistake instead of recognising the approach is wrong.
- **Long runs.** Context from the start of a task quietly decays by the end.

If your tool allows it, disable automatic script execution. Review what is
about to run.

### The argument not worth having

People argue endlessly about whether AI will replace developers. If it gets
good enough to replace software engineers, most other knowledge work goes
too, so worrying about it specifically does not help.

Do not worry. Learn to use the tools well. Developers who understand
prompting, context engineering and AI assisted workflows will have a large
advantage over developers who ignore all of it. The tools still make
mistakes. Used properly they are an enormous multiplier.

The lesson underneath is the same one as Chapter Four: coverage versus
uncovering. Knowing every tool is coverage. Knowing which one to reach for,
and why, is the other thing.

import Link from "next/link";

export default function Header() {
  return (
    <header className="border-b border-foreground/10">
      <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-4 py-4">
        {/* Site name links back to the home page */}
        <Link href="/" className="text-xl font-bold text-emerald-600">
          SplitUnwise
        </Link>

        {/* Navigation links */}
        <nav aria-label="Main">
          <ul className="flex flex-wrap items-center gap-6 text-sm font-medium">
            <li>
              <Link href="/dashboard" className="hover:text-emerald-600">
                Dashboard
              </Link>
            </li>
            <li>
              <Link href="/groups" className="hover:text-emerald-600">
                Groups
              </Link>
            </li>
            <li>
              <Link href="/friends" className="hover:text-emerald-600">
                Friends
              </Link>
            </li>
            <li>
              <Link href="/activity" className="hover:text-emerald-600">
                Activity
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
